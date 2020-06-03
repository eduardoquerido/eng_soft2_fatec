import zipfile

from tempfile import NamedTemporaryFile

from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.http import FileResponse


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
