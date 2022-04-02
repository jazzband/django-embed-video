import os

import django

os.environ["DJANGO_SETTINGS_MODULE"] = "embed_video.tests.django_settings"

django.setup()
