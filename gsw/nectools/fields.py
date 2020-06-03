from django.conf import settings
from django.db.models import FileField
from django.forms import CharField
from django.forms import FileField as FormFileField
from django.forms import ValidationError
from django.template.defaultfilters import filesizeformat


from .utils.cpf import CPF


MAX_UPLOAD_SIZE = 5242880
CONTENT_TYPES = [
    # 'application/msword',  # Microsoft Word
    'application/pdf',  # Adobe Portable Document Format
    # 'application/rtf',  # Rich Text Format
    # 'application/vnd.ms-excel',  # Microsoft Excel
    # 'application/vnd.ms-powerpoint',  # Microsoft PowerPoint
    # 'application/vnd.oasis.opendocument.spreadsheet',  # OpenDocument Spreadsheet
    # 'application/vnd.oasis.opendocument.text',  # OpenDocument Text
    # 'application/vnd.openxmlformats-officedocument.presentationml.slideshow',  # Microsoft Office - OOXML - Presentation (Slideshow)
    # 'application/vnd.openxmlformats-officedocument.presentationml.slide',  # Microsoft Office - OOXML - Presentation (Slide)
    # 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # Microsoft Office - OOXML - Spreadsheet
    # 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # Microsoft Office - OOXML - Word Document
    # 'application/vnd.sun.xml.draw',  # OpenOffice - Draw (Graphics)
    # 'application/x-mswrite',  # Microsoft Wordpad
    # 'application/x-tar',  # TAR
    # 'application/zip',  # ZIP
    'image/bmp',  # BMP
    # 'image/gif',  # GIF
    'image/jpeg',  # JPG/JPEG
    'image/png',  # PNG
    # 'image/svg+xml',  # SVG
    # 'text/plain',  # text
    # 'text/richtext',  # Rich Text Format (RTF)
]


CONTENT_TYPES = getattr(settings, 'DOCUMENT_CONTENT_TYPES', CONTENT_TYPES)
MAX_UPLOAD_SIZE = getattr(settings, 'DOCUMENT_MAX_UPLOAD_SIZE', MAX_UPLOAD_SIZE)


class ContentTypeRestrictedFormFileField(FormFileField):
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", CONTENT_TYPES)
        self.max_upload_size = kwargs.pop("max_upload_size", MAX_UPLOAD_SIZE)
        super(ContentTypeRestrictedFormFileField, self).__init__(*args, **kwargs)

    def clean(self, value, initial=None, *args, **kwargs):
        data = super(ContentTypeRestrictedFormFileField, self).clean(value, initial, *args, **kwargs)
        if not data:
            return data
        elif initial:
            return initial
        try:
            content_type = data.content_type
            if data.size > self.max_upload_size:
                raise ValidationError(
                    u'Por favor, mantenha o tamanho do arquivo abaixo de %s. Tamanho atual do arquivo %s' % (
                        filesizeformat(self.max_upload_size),
                        filesizeformat(data.size)
                    )
                )
            elif self.content_types and content_type not in self.content_types:
                raise ValidationError(u'O tipo do arquivo (%s) não é suportado' % content_type)
        except AttributeError:
            pass
        return data


class ContentTypeRestrictedFileField(FileField):
    """
        restringe os arquivos
        por tamanho e por tipo
        10KB  - 10240
        50KB  - 51200
        100KB - 102400
        1MB   - 1048576
        2MB   - 2097152
        5MB   - 5242880
        10MB  - 10485760
        20MB  - 20971520
        50MB  - 52428800
        100MB - 104857600
        250MB - 262144000
        500MB - 524288000
    """

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", CONTENT_TYPES)
        self.max_upload_size = kwargs.pop("max_upload_size", MAX_UPLOAD_SIZE)
        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.
        defaults = {'form_class': ContentTypeRestrictedFormFileField}
        defaults.update(kwargs)
        defaults['content_types'] = self.content_types
        defaults['max_upload_size'] = self.max_upload_size
        return super(ContentTypeRestrictedFileField, self).formfield(**defaults)


class CPFField(CharField):
    def __init__(self, max_length=14, min_length=11, *args, **kwargs):
        super(CPFField, self).__init__(max_length=max_length, min_length=min_length, *args, **kwargs)

    def clean(self, value):
        value = super(CPFField, self).clean(value)
        if not value and not self.required:
            return None
        try:
            cpf = CPF(value)
        except Exception:
            raise ValidationError('CPF Inválido')
        if cpf.valido():
            return cpf.sem_formato()
        raise ValidationError('CPF Inválido')
