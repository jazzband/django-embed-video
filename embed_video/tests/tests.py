import os

from unittest import main

os.environ['DJANGO_SETTINGS_MODULE'] = 'embed_video.tests.django_settings'

from tests_fields import EmbedVideoFieldTestCase, EmbedVideoFormFieldTestCase
from tests_backend import EmbedVideoTestCase
