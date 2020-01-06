import requests
from unittest import TestCase
from unittest.mock import patch

from . import BackendTestMixin
from embed_video.backends import VimeoBackend, VideoDoesntExistException


class VimeoBackendTestCase(BackendTestMixin, TestCase):
    urls = (
        ("http://vimeo.com/72304002", "72304002"),
        ("https://vimeo.com/72304002", "72304002"),
        ("http://www.vimeo.com/72304002", "72304002"),
        ("https://www.vimeo.com/72304002", "72304002"),
        ("http://player.vimeo.com/video/72304002", "72304002"),
        ("https://player.vimeo.com/video/72304002", "72304002"),
        ("http://www.vimeo.com/channels/staffpick/72304002", "72304002"),
        ("https://www.vimeo.com/channels/staffpick/72304002", "72304002"),
        ("https://vimeo.com/exampleusername/review/72304002/a1b2c3d4", "72304002"),
    )

    instance = VimeoBackend

    def test_vimeo_get_info_exception(self):
        with self.assertRaises(VideoDoesntExistException):
            backend = VimeoBackend("https://vimeo.com/123")
            backend.get_info()

    def test_get_thumbnail_url(self):
        backend = VimeoBackend("https://vimeo.com/72304002")
        self.assertEqual(
            backend.get_thumbnail_url(),
            "https://i.vimeocdn.com/video/446150690_640.jpg",
        )

    @patch("embed_video.backends.EMBED_VIDEO_TIMEOUT", 0.000001)
    def test_timeout_in_get_info(self):
        backend = VimeoBackend("https://vimeo.com/72304002")
        self.assertRaises(requests.Timeout, backend.get_info)
