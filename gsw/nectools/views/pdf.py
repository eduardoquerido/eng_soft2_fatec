# coding: utf-8

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic.base import View

from django_xhtml2pdf.utils import generate_pdf


class PDFView(View):
    '''
        View que gera um PDF usando a lib django_xhtml2pdf
    '''
    template_name = None
    file_name = None
    obj_context_name = 'object'
    pk_url_kwarg = 'pk'
    model = None
    force_attachment_download = True

    def get_template_names(self):
        return self.template_name

    def get_file_name(self):
        if not self.file_name:
            return self.obj_context_name + ('_%s.pdf' % self.object.pk)
        return self.file_name

    def get_context_data(self, **kwargs):
        return {
            'object': self.object,
            self.obj_context_name: self.object
        }

    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs[self.pk_url_kwarg])

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        resp = HttpResponse(content_type='application/pdf')
        if self.force_attachment_download:
            resp['Content-Disposition'] = 'attachment; filename=%s' % self.get_file_name()

        return generate_pdf(
            self.get_template_names(),
            file_object=resp,
            context=self.get_context_data()
        )
