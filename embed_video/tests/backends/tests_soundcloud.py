from unittest import TestCase
from unittest.mock import patch

import requests

from embed_video.backends import SoundCloudBackend, VideoDoesntExistException
from embed_video.tests.backends import BackendTestMixin


class SoundCloudBackendTestCase(BackendTestMixin, TestCase):
    urls = (
        ("https://soundcloud.com/community/soundcloud-case-study-wildlife", "82244706"),
        (
            "https://soundcloud.com/matej-roman/jaromir-nohavica-karel-plihal-mikymauz",
            "7834701",
        ),
        ("https://soundcloud.com/beny97/sets/jaromir-nohavica-prazska", "960591"),
        (
            "https://soundcloud.com/jet-silver/couleur-3-downtown-boogie-show-prove",
            "257485194",
        ),
    )

    instance = SoundCloudBackend

    def setUp(self):
        class FooBackend(SoundCloudBackend):
            url = "foobar"

            def get_info(self):
                return {
                    "width": 123,
                    "height": 321,
                    "thumbnail_url": "xyz",
                    "html": '\u003Ciframe width="100%" height="400" '
                    'scrolling="no" frameborder="no" '
                    'src="{0}"\u003E\u003C/iframe\u003E'.format(self.url),
                }

        self.foo = FooBackend("abcd")

    def test_width(self):
        self.assertEqual(self.foo.width, 123)

    def test_height(self):
        self.assertEqual(self.foo.height, 321)

    def test_get_thumbnail_url(self):
        self.assertEqual(self.foo.get_thumbnail_url(), "xyz")

    def test_get_url(self):
        self.assertEqual(self.foo.get_url(), self.foo.url)

    @patch("embed_video.backends.EMBED_VIDEO_TIMEOUT", 0.000001)
    def test_timeout_in_get_info(self):
        backend = SoundCloudBackend(
            "https://soundcloud.com/community/soundcloud-case-study-wildlife"
        )
        self.assertRaises(requests.Timeout, backend.get_info)

    def test_invalid_url(self):
        """Check if bug #21 is fixed."""
        backend = SoundCloudBackend("https://soundcloud.com/xyz/foo")
        self.assertRaises(VideoDoesntExistException, backend.get_info)
