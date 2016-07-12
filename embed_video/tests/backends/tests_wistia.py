import requests
from mock import patch
from unittest import TestCase

from . import BackendTestMixin
from embed_video.backends import WistiaBackend, VideoDoesntExistException


class WistiaBackendTestCase(BackendTestMixin, TestCase):

    urls = (
        ('https://support.wistia.com/medias/26sk4lmiix', '26sk4lmiix'),  # This comes from the wistia docs
    )

    instance = WistiaBackend

    def test_wistia_get_info_exception(self):
        with self.assertRaises(VideoDoesntExistException):
            backend = WistiaBackend('http://gxsc.wistia.com/123')
            backend.get_info()

    def test_get_thumbnail_url(self):
        backend = WistiaBackend('https://gxsc.wistia.com/medias/2y1o2i2vx6')
        self.assertEqual(backend.get_thumbnail_url(),
                         'https://embed-ssl.wistia.com/deliveries/14fb3042a6df04d57a6ed1a659f737d30b6d9e5c.jpg?image_crop_resized=1920x1080')

    @patch('embed_video.backends.EMBED_VIDEO_TIMEOUT', 0.000001)
    def test_timeout_in_get_info(self):
        backend = WistiaBackend('http://support.wistia.com/72304002')
        self.assertRaises(requests.Timeout, backend.get_info)
