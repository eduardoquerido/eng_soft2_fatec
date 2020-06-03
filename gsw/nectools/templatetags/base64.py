import base64
from io import BytesIO
from PIL import Image

from django import template
from django.conf import settings


register = template.Library()

EMPTY_IMG = (
    "data:image/png;base64,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"
)


@register.filter
def file_field_to_image64(file):
    output = BytesIO()
    try:
        img = Image.open(open(file.path, 'rb'))
        img.save(output, 'png')
        return "data:image/png;base64,%s" % str(base64.b64encode(output.getvalue()), 'utf-8')
    except (IOError, UnboundLocalError, FileNotFoundError):
        # raise IOError(u"O arquivo %s não foi encontrado no media" % file.path)
        return EMPTY_IMG


@register.filter
def image_to_image64(file_path):
    output = BytesIO()
    for dir_ in settings.STATICFILES_DIRS:
        try:
            img = Image.open(open(dir_ + '/' + file_path, 'rb'))
            break
        except (IOError, UnboundLocalError, FileNotFoundError):
            pass
    try:
        img.save(output, 'png')
        return "data:image/png;base64,%s" % str(base64.b64encode(output.getvalue()), 'utf-8')
    except (IOError, UnboundLocalError, FileNotFoundError):
        return EMPTY_IMG
