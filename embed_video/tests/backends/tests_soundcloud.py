from json import dumps
from unittest import TestCase
from unittest.mock import patch

import requests
import requests_mock

from embed_video.backends import (
    SoundCloudBackend,
    VideoDoesntExistException,
    detect_backend,
)


class SoundCloudBackendTestCase(TestCase):
    urls = (
        (
            "https://soundcloud.com/community/soundcloud-case-study-wildlife",
            "82244706",
            "https://soundcloud.com/oembed?format=json&url=https%3A%2F%2Fsoundcloud.com%2Fcommunity%2Fsoundcloud-case-study-wildlife",
            dumps(
                {
                    "version": 1.0,
                    "type": "rich",
                    "provider_name": "SoundCloud",
                    "provider_url": "https://soundcloud.com",
                    "height": 400,
                    "width": "100%",
                    "title": "SoundCloud Case Study: Wildlife Control by SoundCloud Community",
                    "description": "Listen to how Wildlife Control makes the most of the SoundCloud platform, and it's API.",
                    "thumbnail_url": "https://i1.sndcdn.com/artworks-000042390403-ouou1g-t500x500.jpg",
                    "html": '<iframe width="100%" height="400" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?visual=true&url=https%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F82244706&show_artwork=true"></iframe>',
                    "author_name": "SoundCloud Community",
                    "author_url": "https://soundcloud.com/community",
                }
            ),
        ),
        (
            "https://soundcloud.com/matej-roman/jaromir-nohavica-karel-plihal-mikymauz",
            "7834701",
            "https://soundcloud.com/oembed?format=json&url=https%3A%2F%2Fsoundcloud.com%2Fmatej-roman%2Fjaromir-nohavica-karel-plihal-mikymauz",
            dumps(
                {
                    "version": 1.0,
                    "type": "rich",
                    "provider_name": "SoundCloud",
                    "provider_url": "https://soundcloud.com",
                    "height": 400,
                    "width": "100%",
                    "title": "Jaromír Nohavica, Karel Plíhal - Mikymauz by Matěj Roman",
                    "description": "",
                    "thumbnail_url": "https://soundcloud.com/images/fb_placeholder.png",
                    "html": '<iframe width="100%" height="400" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?visual=true&url=https%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F7834701&show_artwork=true"></iframe>',
                    "author_name": "Matěj Roman",
                    "author_url": "https://soundcloud.com/matej-roman",
                }
            ),
        ),
        (
            "https://soundcloud.com/beny97/sets/jaromir-nohavica-prazska",
            "960591",
            "https://soundcloud.com/oembed?format=json&url=https%3A%2F%2Fsoundcloud.com%2Fbeny97%2Fsets%2Fjaromir-nohavica-prazska",
            dumps(
                {
                    "version": 1.0,
                    "type": "rich",
                    "provider_name": "SoundCloud",
                    "provider_url": "https://soundcloud.com",
                    "height": 450,
                    "width": "100%",
                    "title": "Jaromir Nohavica - Prazska palena by beny97",
                    "description": "",
                    "thumbnail_url": "https://soundcloud.com/images/fb_placeholder.png",
                    "html": '<iframe width="100%" height="450" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?visual=true&url=https%3A%2F%2Fapi.soundcloud.com%2Fplaylists%2F960591&show_artwork=true"></iframe>',
                    "author_name": "beny97",
                    "author_url": "https://soundcloud.com/beny97",
                }
            ),
        ),
        (
            "https://soundcloud.com/jet-silver/couleur-3-downtown-boogie-show-prove",
            "257485194",
            "https://soundcloud.com/oembed?format=json&url=https%3A%2F%2Fsoundcloud.com%2Fjet-silver%2Fcouleur-3-downtown-boogie-show-prove",
            dumps(
                {
                    "version": 1.0,
                    "type": "rich",
                    "provider_name": "SoundCloud",
                    "provider_url": "https://soundcloud.com",
                    "height": 400,
                    "width": "100%",
                    "title": "Couleur 3 - Downtown Boogie : Show & Prove by Jet Silver",
                    "description": "Show & Prove specially recorded for Downtown Boogie, the best hip-hop radio show in Switzerland, on Couleur 3 radio. Shout out to Vincz Lee, Jiggy Jones, Green Giant, Dynamike and Geos for having us one the ones and twos !",
                    "thumbnail_url": "https://i1.sndcdn.com/artworks-000156604478-47oo6y-t500x500.jpg",
                    "html": '<iframe width="100%" height="400" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?visual=true&url=https%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F257485194&show_artwork=true"></iframe>',
                    "author_name": "Jet Silver",
                    "author_url": "https://soundcloud.com/jet-silver",
                }
            ),
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

    def test_detect(self):
        for url in self.urls:
            with requests_mock.Mocker() as m:
                m.get(url[2], text=url[3])
                backend = detect_backend(url[0])
                self.assertIsInstance(backend, self.instance)

    def test_code(self):
        for url in self.urls:
            with requests_mock.Mocker() as m:
                m.get(url[2], text=url[3])
                backend = self.instance(url[0])
                self.assertEqual(backend.code, url[1])

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
