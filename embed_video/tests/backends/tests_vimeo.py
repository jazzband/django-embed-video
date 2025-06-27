import urllib.parse
from unittest import TestCase
from unittest.mock import patch

import requests

from embed_video.backends import VideoDoesntExistException, VimeoBackend, detect_backend


class VimeoBackendTestCase(TestCase):
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
        ("https://vimeo.com/manage/72304002/general", "72304002"),
    )

    instance = VimeoBackend

    def test_detect(self):
        for url in self.urls:
            backend = detect_backend(url[0])
            self.assertIsInstance(backend, self.instance)

    def test_code(self):
        for url in self.urls:
            backend = self.instance(url[0])
            self.assertEqual(backend.code, url[1])

    def test_vimeo_get_info_exception(self):
        with self.assertRaises(VideoDoesntExistException):
            backend = VimeoBackend("https://vimeo.com/123")
            backend.get_info()

    def test_get_thumbnail_url(self):
        backend = VimeoBackend("https://vimeo.com/72304002")
        expected_url = "https://i.vimeocdn.com/video/446150690-9621b882540b53788eaa36ef8e303d4e06fc40af3d27918b7f561bb44ed971dc-d_640"
        actual_url = backend.get_thumbnail_url()
        # Parse URLs and compare without query parameters
        expected_parts = urllib.parse.urlparse(expected_url)
        actual_parts = urllib.parse.urlparse(actual_url)
        # Compare scheme, netloc, and path only
        self.assertEqual(
            (expected_parts.scheme, expected_parts.netloc, expected_parts.path),
            (actual_parts.scheme, actual_parts.netloc, actual_parts.path),
        )

    @patch("embed_video.backends.EMBED_VIDEO_TIMEOUT", 0.000001)
    def test_timeout_in_get_info(self):
        backend = VimeoBackend("https://vimeo.com/72304002")
        self.assertRaises(requests.Timeout, backend.get_info)
