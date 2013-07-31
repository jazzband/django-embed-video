import os

from unittest import main, TestCase

from django.http import HttpRequest
from django.template.base import Template
from django.template.context import RequestContext

from ..fields import EmbedVideoField, EmbedVideoFormField

os.environ['DJANGO_SETTINGS_MODULE'] = 'embed_video.tests.django_settings'


class EmbedVideoFieldsTestCase(TestCase):
    def test_field_validation(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    main()
