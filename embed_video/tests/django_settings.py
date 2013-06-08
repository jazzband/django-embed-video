import os

from django.conf.global_settings import *

DEBUG = True
SECRET_KEY = 'testing_key123'

STATIC_ROOT = MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static')
STATIC_URL = MEDIA_URL = '/static/'

INSTALLED_APPS = (
    'embed_video',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'less': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
