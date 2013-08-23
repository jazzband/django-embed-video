# Django settings for example_project project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'example_project.sqlite3',
    }
}

SITE_ID = 1

SECRET_KEY = 'u%38dln@$1!7w#cxi4np504^sa3_skv5aekad)jy_u0v2mc+nr'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


ROOT_URLCONF = 'example_project.urls'


DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
)

THIRD_PARTY_APPS = (
    'embed_video',
)

LOCAL_APPS = (
    'example_project',
    'posts',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
