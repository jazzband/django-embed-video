from unittest import TestCase
from mock import patch
import requests

from ..backends import detect_backend, YoutubeBackend, VimeoBackend, \
    SoundCloudBackend, UnknownBackendException, VideoDoesntExistException, \
    UnknownIdException, VideoBackend


class BackendTestMixin(object):
    def test_detect(self):
        for url in self.urls:
            backend = detect_backend(url[0])
            self.assertIsInstance(backend, self.instance)

    def test_code(self):
        for url in self.urls:
            backend = self.instance(url[0])
            self.assertEqual(backend.code, url[1])


class VideoBackendTestCase(TestCase):
    unknown_backend_urls = (
        'http://myurl.com/?video=http://www.youtube.com/watch?v=jsrRJyHBvzw',
        'http://myurl.com/?video=www.youtube.com/watch?v=jsrRJyHBvzw',
        'http://youtube.com.myurl.com/watch?v=jsrRJyHBvzw',
        'http://vimeo.com.myurl.com/72304002',
    )

    def test_detect_bad_urls(self):
        for url in self.unknown_backend_urls:
            self.assertRaises(UnknownBackendException, detect_backend, url)

    def test_not_implemented_get_info(self):
        backend = VideoBackend('http://www.example.com')
        self.assertRaises(NotImplementedError, backend.get_info)


class YoutubeBackendTestCase(BackendTestMixin, TestCase):
    urls = (
        ('http://youtu.be/jsrRJyHBvzw', 'jsrRJyHBvzw'),
        ('http://youtu.be/n17B_uFF4cA', 'n17B_uFF4cA'),
        ('http://youtu.be/t-ZRX8984sc', 't-ZRX8984sc'),
        ('https://youtu.be/t-ZRX8984sc', 't-ZRX8984sc'),
        ('http://youtube.com/watch?v=jsrRJyHBvzw', 'jsrRJyHBvzw'),
        ('https://youtube.com/watch?v=jsrRJyHBvzw', 'jsrRJyHBvzw'),
        ('http://www.youtube.com/v/0zM3nApSvMg?rel=0', '0zM3nApSvMg'),
        ('https://www.youtube.com/v/0zM3nApSvMg?rel=0', '0zM3nApSvMg'),
        ('http://www.youtube.com/embed/0zM3nApSvMg?rel=0', '0zM3nApSvMg'),
        ('https://www.youtube.com/embed/0zM3nApSvMg?rel=0', '0zM3nApSvMg'),
        ('http://www.youtube.com/watch?v=jsrRJyHBvzw', 'jsrRJyHBvzw'),
        ('https://www.youtube.com/watch?v=t-ZRX8984sc', 't-ZRX8984sc'),
        ('http://www.youtube.com/watch?v=iwGFalTRHDA&feature=related', 'iwGFalTRHDA'),
        ('https://www.youtube.com/watch?v=iwGFalTRHDA&feature=related', 'iwGFalTRHDA'),
        ('http://www.youtube.com/watch?feature=player_embedded&v=2NpZbaAIXag', '2NpZbaAIXag'),
        ('https://www.youtube.com/watch?feature=player_embedded&v=2NpZbaAIXag', '2NpZbaAIXag'),
        ('https://www.youtube.com/watch?v=XPk521voaOE&feature=youtube_gdata_player', 'XPk521voaOE'),
        ('http://www.youtube.com/watch?v=6xu00J3-g2s&list=PLb5n6wzDlPakFKvJ69rJ9AJW24Aaaki2z', '6xu00J3-g2s'),
        ('https://m.youtube.com/#/watch?v=IAooXLAPoBQ', 'IAooXLAPoBQ'),
        ('https://m.youtube.com/watch?v=IAooXLAPoBQ', 'IAooXLAPoBQ')
    )

    instance = YoutubeBackend

    def test_youtube_keyerror(self):
        """ Test for issue #7 """
        backend = self.instance('http://youtube.com/watch?id=5')
        self.assertRaises(UnknownIdException, backend.get_code)

    def test_thumbnail(self):
        for url in self.urls:
            backend = self.instance(url[0])
            self.assertIn(url[1], backend.thumbnail)


class VimeoBackendTestCase(BackendTestMixin, TestCase):
    urls = (
        ('http://vimeo.com/72304002', '72304002'),
        ('https://vimeo.com/72304002', '72304002'),
        ('http://www.vimeo.com/72304002', '72304002'),
        ('https://www.vimeo.com/72304002', '72304002'),
        ('http://player.vimeo.com/video/72304002', '72304002'),
        ('https://player.vimeo.com/video/72304002', '72304002'),
    )

    instance = VimeoBackend

    def test_vimeo_get_info_exception(self):
        with self.assertRaises(VideoDoesntExistException):
            backend = VimeoBackend('http://vimeo.com/123')
            backend.get_info()

    def test_get_thumbnail_url(self):
        backend = VimeoBackend('http://vimeo.com/72304002')
        self.assertEqual(backend.get_thumbnail_url(),
                         'http://i.vimeocdn.com/video/446150690_640.jpg')

    @patch('embed_video.backends.EMBED_VIDEO_TIMEOUT', 0.000001)
    def test_timeout_in_get_info(self):
        backend = VimeoBackend('http://vimeo.com/72304002')
        self.assertRaises(requests.Timeout, backend.get_info)


class SoundCloudBackendTestCase(BackendTestMixin, TestCase):
    urls = (
        ('https://soundcloud.com/community/soundcloud-case-study-wildlife', '82244706'),
        ('https://soundcloud.com/matej-roman/jaromir-nohavica-karel-plihal-mikymauz', '7834701'),
        ('https://soundcloud.com/beny97/sets/jaromir-nohavica-prazska', '960591'),
        ('https://soundcloud.com/corbel-keep/norah-jones-come-away-with', '22485933'),
    )

    instance = SoundCloudBackend

    def setUp(self):
        class FooBackend(SoundCloudBackend):
            url = 'foobar'

            def get_info(self):
                return {
                    'width': 123,
                    'height': 321,
                    'thumbnail_url': 'xyz',
                    'html': u'\u003Ciframe width=\"100%\" height=\"400\" '
                            u'scrolling=\"no\" frameborder=\"no\" '
                            u'src=\"{0}\"\u003E\u003C/iframe\u003E'.format(self.url)
                }

        self.foo = FooBackend('abcd')

    def test_width(self):
        self.assertEqual(self.foo.width, 123)

    def test_height(self):
        self.assertEqual(self.foo.height, 321)

    def test_get_thumbnail_url(self):
        self.assertEqual(self.foo.get_thumbnail_url(), 'xyz')

    def test_get_url(self):
        self.assertEqual(self.foo.get_url(), self.foo.url)

    def test_get_embed_code(self):
        self.assertEqual(self.foo.get_embed_code(100, 200),
                         u'<iframe width="100" height="321" src="foobar"'
                         u'\n        frameborder="0" allowfullscreen>'
                         u'</iframe>\n')

    @patch('embed_video.backends.EMBED_VIDEO_TIMEOUT', 0.000001)
    def test_timeout_in_get_info(self):
        backend = SoundCloudBackend('https://soundcloud.com/community/soundcloud-case-study-wildlife')
        self.assertRaises(requests.Timeout, backend.get_info)

    def test_invalid_url(self):
        """ Check if bug #21 is fixed. """
        backend = SoundCloudBackend('https://soundcloud.com/xyz/foo')
        self.assertRaises(VideoDoesntExistException, backend.get_info)
