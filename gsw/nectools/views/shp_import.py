import os
import tempfile
import zipfile

try:
    from cStringIO import StringIO as SIO
except Exception:
    from io import BytesIO as SIO

from datetime import datetime

from chardet.universaldetector import UniversalDetector

from django import forms
from django.utils.encoding import force_text
from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.views.generic.edit import CreateView
from django.contrib.gis.geos import (
    Polygon,
    MultiPolygon,
    Point,
    LineString,
    MultiPoint,
    MultiLineString,
)


ZIP_MIMETYPES = (
    'application/zip',
    'application/x-zip',
    'application/x-zip-compressed',
    'application/octet-stream',
    'application/x-compress',
    'application/x-compressed',
    'multipart/x-zip',
)


def guess_encoding(path_shp):
    # TODO detectar um .dbf na pasta do shp e pegar o nome dele
    path_dbf = '%sdbf' % path_shp[:-3]
    detector = UniversalDetector()
    for line in open(path_dbf, 'rb'):
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']


def rmdir_files(dirpath):
    for f in os.listdir(dirpath):
        os.remove(os.path.join(dirpath, f))
    os.rmdir(dirpath)


class ImportShapeView(CreateView):
    '''Class Based View que importa um Shape File para um modelo do Django
    cada feature vira uma tupla no BD

    usa o ShapeForm que é um formulário com um campo arquivo que recebe um shp
    e salva as features como instâncias no BD

    o atributo map fields é uma lista de tuplas com model_field, feature_field, converte_func
    onde model_field é uma string com o nome do campo no modelo
    feature_field é o nome da coluna no Shape File
    e converte_func é uma função que converte o tipo do Shape file para o tipo do Modelo
    '''
    template_name_suffix = '_shp_import_form'
    geom_field = 'geom'
    geom_type = 'Polygon'
    multi = True
    map_fields = None
    model = None
    success_url = ''

    def get_form_class(self):
        return ShapeForm

    def get_success_url(self):
        return self.success_url

    def get_form_kwargs(self):
        kwargs = super(ImportShapeView, self).get_form_kwargs()
        kwargs['geom_field'] = self.geom_field
        kwargs['geom_type'] = self.geom_type
        kwargs['multi'] = self.multi
        kwargs['request_user'] = self.request.user
        kwargs['map_fields'] = self.map_fields
        kwargs['model'] = self.model
        return kwargs


class ShapeForm(forms.Form):
    '''ShapeForm é um formulário com um campo arquivo que recebe um shp
    e salva as features como instâncias no BD
    '''
    arquivo = forms.FileField(label=u"Shape file para Importação", required=True)

    def __init__(self, *args, **kwargs):
        self.layer = []
        kwargs.pop('instance')
        self.geom_field = kwargs.pop('geom_field', 'geom')
        self.request_user = kwargs.pop('request_user', 'geom')
        self.geom_type = kwargs.pop('geom_type', 'Polygon')
        self.multi = kwargs.pop('multi', True)
        self.map_fields = kwargs.pop('map_fields', [])
        self.model = kwargs.pop('model')
        super(ShapeForm, self).__init__(*args, **kwargs)

    def get_geom(self, feature):
        '''Recupera a geometria de uma feature
        '''
        geom = feature.geom.transform(settings.SRID, clone=True).geos
        if self.multi:
            if isinstance(geom, Polygon):
                geom = MultiPolygon(*[geom])
            elif isinstance(geom, Point):
                geom = MultiPoint(*[geom])
            elif isinstance(geom, LineString):
                geom = MultiLineString(*[geom])
        return geom

    def get_feature_value(self, feature, feature_field):
        '''recupera o valor que vai pro BD vindo do SHP
        '''
        v = feature.get(
            feature_field
        )
        try:
            return v.encode('utf-8')
        except Exception:
            return v

    def set_field_instance(self, instance, model_field, feature, feature_field, converte_func):
        '''Seta em um campo de uma instância um valor de uma coluna do SHP
        '''
        if converte_func == str:
            converte_func = force_text
        setattr(
            instance,
            model_field,
            converte_func(
                self.get_feature_value(feature, feature_field)
            )
        )

    def get_instance(self, feature):
        '''recupera uma instância que será salva no BD
        vinda do SHP
        '''
        instance = self.model()
        instance.user_add = self.request_user
        instance.user_upd = self.request_user
        setattr(instance, self.geom_field, self.get_geom(feature))

        for model_field, feature_field, converte_func in self.map_fields:
            self.set_field_instance(
                instance,
                model_field,
                feature,
                feature_field,
                converte_func,
            )
        return instance

    def save(self, commit=True):
        '''Salva as instâncias do SHP para o BD
        retorna uma lista de intâncias salvas
        '''
        instances = []
        for feature in self.cleaned_data['arquivo']:
            instance = self.get_instance(feature)
            instance.save()
            instances.append(instance)
        return instances

    def clean_arquivo(self):
        '''
            Clean para Upload de ShapeFiles
            arquivo ZIP contendo da raiz um arquivo
            .dbf, .shx, .prj e um .shp
        '''
        layer = []
        arquivo = self.cleaned_data['arquivo']
        if arquivo:
            if isinstance(arquivo, (InMemoryUploadedFile, TemporaryUploadedFile)):
                if arquivo.content_type not in ZIP_MIMETYPES:
                    raise forms.ValidationError("Arquivo não está no formato zip!")
                else:
                    arq_content = SIO()
                    for chunk in arquivo.chunks():
                        arq_content.write(chunk)
                    try:
                        zfile = zipfile.ZipFile(arq_content)
                    except Exception:
                        raise forms.ValidationError("Arquivo não está no formato zip ou está corrompido!")
                    badzip = zfile.testzip()
                    if badzip is not None:
                        raise forms.ValidationError("Arquivo '%s' está corrompido!" % badzip)

                    shpfilename = None
                    zipnamelist = [n.lower() for n in zfile.namelist()]
                    for filename in zipnamelist:
                        if '/' in filename:
                            raise forms.ValidationError("O arquivo contém um diretório. Adicione os arquivos .shp, .dbf, .shx .prj na raiz do diretório.")
                        if filename.endswith('.shp'):
                            shpfilename = filename
                    if not shpfilename:
                        raise forms.ValidationError("O arquivo zip não contém um arquivo .shp")
                    else:
                        shpfilename_base = shpfilename.split('.')[0]
                        for ext in ['dbf', 'shx', 'prj']:
                            if '%s.%s' % (shpfilename_base, ext) not in zipnamelist:
                                raise forms.ValidationError("O arquivo zip não contém um arquivo %s!" % ext)

                    dirpath = os.path.join(
                        tempfile.gettempdir(),
                        self.model.__module__.split('.')[-1],
                        "shape",
                        "temp",
                        ''.join(map(str, datetime.now().timetuple()))
                    )
                    if not os.path.exists(dirpath):
                        os.makedirs(dirpath)
                    for filename in zfile.namelist():
                        fd = open(os.path.join(dirpath, filename.lower()), 'wb')
                        fd.write(zfile.read(filename))
                        fd.close()
                    zfile.close()

                    shp_file_path = os.path.join(dirpath, shpfilename.lower())
                    guessed_encoding = guess_encoding(shp_file_path)
                    if guessed_encoding:
                        ds = DataSource(shp_file_path, encoding=guessed_encoding)
                    else:
                        ds = DataSource(shp_file_path)

                    if len(ds):
                        layer = ds[0]
                        # verifica se arquivo possui atributos que foram mapeados
                        keys_fields = [map_field[1] for map_field in self.map_fields]
                        if keys_fields and not (set(keys_fields).intersection(set(layer.fields))):
                            raise forms.ValidationError('O shape deve conter o(s) seguinte(s) atributo(s): %s' % ', '.join(keys_fields))
                        if not layer.srs.proj4:
                            # apaga dir temp
                            rmdir_files(dirpath)
                            raise forms.ValidationError("Não foi possível determinar a projeção deste shape!")
                        if self.geom_type in ('Polygon', 'Point', 'LineString'):
                            if not self.multi:
                                if layer.geom_type.name not in (self.geom_type, '%s25D' % self.geom_type):
                                    # apaga dir temp
                                    rmdir_files(dirpath)
                                    raise forms.ValidationError("Este shape não contém %s!" % self.geom_type)

                            elif layer.geom_type.name not in (self.geom_type, '%s25D' % self.geom_type, 'Multi%s' % self.geom_type, 'Multi%s25D' % self.geom_type):
                                # apaga dir temp
                                rmdir_files(dirpath)
                                raise forms.ValidationError("Este shape não contém %s!" % self.geom_type)
                    else:
                        # apaga dir temp
                        rmdir_files(dirpath)
                        raise forms.ValidationError("Shapefile vazio!")
        return layer
