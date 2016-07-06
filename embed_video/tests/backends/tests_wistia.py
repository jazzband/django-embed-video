import requests
from mock import patch
from unittest import TestCase

from . import BackendTestMixin
from embed_video.backends import WistiaBackend, VideoDoesntExistException


class WistiaBackendTestCase(BackendTestMixin, TestCase):

    urls = (
        # ('https://gxsc.wistia.com/medias/ed0lahzq9t', 'ed0lahzq9t'),
        # ('https://gxsc.wistia.com/medias/ndfbdn2zi0', 'ndfbdn2zi0'),
        # ('https://gxsc.wistia.com/medias/vcktuzuw5p', 'vcktuzuw5p'),
        ('https://support.wistia.com/medias/26sk4lmiix', '26sk4lmiix'),  # This comes from the wistia docs
        #  ('http://player.vimeo.com/video/72304002', '72304002'), used this as a test
        # ('http://embed.wistia.com/deliveries/5413caeac5fdf4064a2f9eab5c10a0848e42f19f', '5413caeac5fdf4064a2f9eab5c10a0848e42f19f')
    )

    instance = WistiaBackend

    def test_wistia_get_info_exception(self):
        with self.assertRaises(VideoDoesntExistException):
            backend = WistiaBackend('http://gxsc.wistia.com/123')
            backend.get_info()

    def test_get_thumbnail_url(self):
        backend = WistiaBackend('http://embed.wistia.com/deliveries/5413caeac5fdf4064a2f9eab5c10a0848e42f19f')
        self.assertEqual(backend.get_thumbnail_url(),
                         'http://embed.wistia.com/deliveries/5413caeac5fdf4064a2f9eab5c10a0848e42f19f.jpeg?video_still_time=10')

    @patch('embed_video.backends.EMBED_VIDEO_TIMEOUT', 0.000001)
    def test_timeout_in_get_info(self):
        backend = WistiaBackend('http://support.wistia.com/72304002')
        self.assertRaises(requests.Timeout, backend.get_info)
