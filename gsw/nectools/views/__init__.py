import zipfile

from tempfile import NamedTemporaryFile

from django.apps import apps
from django.contrib import messages
from django.contrib.gis.shortcuts import render_to_kml
from django.core.exceptions import ImproperlyConfigured
from django.forms import models as model_forms
from django.http import HttpResponse, JsonResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.edit import DeleteView
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView


from .mixins import CSVMixin
from .mixins import JSONResponseMixin
from .mixins import LoginRequiredMixin
from .mixins import PaginationQueryStringMixin


get_model = apps.get_model


class AddWidgetViewForm(object):
    widgets = None

    def get_form_class(self):
        if self.fields is not None and self.form_class:
            raise ImproperlyConfigured(
                "Specifying both 'fields' and 'form_class' is not permitted."
            )
        if self.form_class:
            return self.form_class
        else:
            if self.model is not None:
                model = self.model
            elif hasattr(self, 'object') and self.object is not None:
                model = self.object.__class__
            else:
                model = self.get_queryset().model
            if self.fields is None:
                raise ImproperlyConfigured(
                    "Using ModelFormMixin (base class of %s) without "
                    "the 'fields' attribute is prohibited." % self.__class__.__name__
                )
            return model_forms.modelform_factory(
                model,
                fields=self.fields,
                widgets=self.widgets
            )


class JSONResponseView(JSONResponseMixin, View):
    def get(self, request, *args, **kwargs):
        return self.render_to_response({})

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class SearchFormListView(PaginationQueryStringMixin, FormMixin, ListView):
    '''
        Classe de view para colocar um filtro
        na ListView
    '''

    http_method_names = ['get']
    filter_by_user = False
    by_user_method = 'by_user'

    def get_form_kwargs(self):
        '''
        este método altera o comportamento padrão do FORMixin.
        Permite o uso do get_initial().
        Carrega no `data` do form o dicionário do `initial`
        quando:
            1. o data está vazio
            2. intial nao é vazio.
            3. methodo http é um get

            ps; thanks to @zokis
        '''

        kw = super().get_form_kwargs()
        kw['data'] = {}
        if self.request.GET:
            kw['data'] = self.request.GET
        elif kw['initial']:
            kw['data'] = kw['initial']
        return kw

    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())

    def get_queryset(self):
        if self.form.is_valid():
            object_list = self.form.get_result_queryset()
        else:
            object_list = self.form.Meta.base_qs.none()

        if self.filter_by_user:
            object_list = getattr(object_list, self.by_user_method)(self.request.user)

        return object_list

    def get(self, request, *args, **kwargs):
        self.form = self.get_form(self.get_form_class())
        self.object_list = self.get_queryset()

        context = self.get_context_data(
            object_list=self.object_list,
            form=self.form,
            url_params=request.GET.urlencode()
        )
        return self.render_to_response(context)


class GenericDeleteFromModel(LoginRequiredMixin, DeleteView):
    def delete(self, request, *args, **kwargs):
        can_delete = True
        obj = self.get_object()
        if hasattr(obj, 'user_can_delete'):
            if not obj.user_can_delete(request.user):
                messages.success(request, "Não foi possível deletar")
                can_delete = False
        elif hasattr(obj, 'can_delete'):
            if not obj.can_delete():
                messages.success(request, "Não foi possível deletar")
                can_delete = False
        if can_delete:
            obj.delete()
            messages.success(request, u"Deletado com sucesso")

        if self.request.GET.get('json', 'false') == 'true':
            return JsonResponse({'success': True})

        return redirect(self.get_success_url())

    def get_success_url(self):
        return self.request.GET.get('next', 'home')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_object(self):
        object_id = self.kwargs['object_id']
        app_name, model_name = self.kwargs['app_model'].split('.', 1)
        model = get_model(app_name, model_name)
        return get_object_or_404(model, pk=object_id)


class ExportCSVView(CSVMixin, View):
    def rows(self):
        raise NotImplementedError


class ZipFileView(View):
    '''
        View que gera um zipfile
    '''
    zip_filename = 'zipfile'
    files = []
    model = None
    pk_url_kwarg = 'pk'
    temp_dir = None

    def get_zip_filename(self):
        return self.zip_filename

    def get_files(self):
        return self.files

    def get_temp_file(self):
        return NamedTemporaryFile(dir=self.temp_dir)

    def zip_files(self):
        zip_temp = self.get_temp_file()
        with zipfile.ZipFile(zip_temp, 'w') as archive:
            for file_path, file_name in self.get_files():
                archive.write(file_path, arcname=file_name)
        zip_temp.seek(0)
        return zip_temp

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, pk=self.kwargs[self.pk_url_kwarg])
        zip_stream = self.zip_files()
        response = FileResponse(
            zip_stream,
            content_type="application/x-zip-compressed"
        )
        response['Content-Disposition'] = 'attachment; filename=%s.zip' % self.get_zip_filename()
        return response


class KMLView(View):
    '''View que responde um KML
    '''
    response_class = HttpResponse

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs):
        response = render_to_kml('gis/kml/placemarks.kml', context)

        # Add header to download as an attachment
        if context.get('download', False):
            response['Content-Disposition'] = (
                'attachment; filename="%s.kml"' % context.get('filename', 'places')
            )
        return response
