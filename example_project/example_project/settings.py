# Django settings for example_project project.

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'example_project.sqlite3',
    }
}

SITE_ID = 1

SECRET_KEY = 'u%38dln@$1!7w#cxi4np504^sa3_skv5aekad)jy_u0v2mc+nr'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

APPEND_SLASH = True

ROOT_URLCONF = 'example_project.urls'

STATIC_URL = '/static/'

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
