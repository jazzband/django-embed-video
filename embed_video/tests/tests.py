import os

from unittest import main

os.environ['DJANGO_SETTINGS_MODULE'] = 'embed_video.tests.django_settings'

from tests_fields import EmbedVideoFieldsTestCase
from tests_backend import EmbedVideoTestCase

if __name__ == '__main__':
    main()
