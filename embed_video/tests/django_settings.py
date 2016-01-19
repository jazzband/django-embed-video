import os

from django.conf.global_settings import *

DEBUG = True
SECRET_KEY = 'testing_key123'

STATIC_ROOT = MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'static')
STATIC_URL = MEDIA_URL = '/static/'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'embed_video',
)


EMBED_VIDEO_BACKENDS = (
    'embed_video.backends.YoutubeBackend',
    'embed_video.backends.VimeoBackend',
    'embed_video.backends.SoundCloudBackend',
    'embed_video.tests.backends.tests_custom_backend.CustomBackend',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'less': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}
