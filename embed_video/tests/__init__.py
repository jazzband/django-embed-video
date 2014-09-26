import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'embed_video.tests.django_settings'

if django.VERSION[:2] >= (1, 7):
    django.setup()