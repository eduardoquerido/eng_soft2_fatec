from .dev import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'uteri',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '54312',
    }
}


