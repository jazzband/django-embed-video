from unittest import TestCase

from ..backends import detect_backend, YoutubeBackend, VimeoBackend, \
        SoundCloudBackend, UnknownBackendException, \
        VideoDoesntExistException, UnknownIdException


class BackendsTestCase(TestCase):
    unknown_backend_urls = (
        'http://myurl.com/?video=http://www.youtube.com/watch?v=jsrRJyHBvzw',
        'http://myurl.com/?video=www.youtube.com/watch?v=jsrRJyHBvzw',
        'http://youtube.com.myurl.com/watch?v=jsrRJyHBvzw',
        'http://vimeo.com.myurl.com/72304002',
    )

    youtube_urls = (
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
    )

    vimeo_urls = (
        ('http://vimeo.com/72304002', '72304002'),
        ('https://vimeo.com/72304002', '72304002'),
        ('http://www.vimeo.com/72304002', '72304002'),
        ('https://www.vimeo.com/72304002', '72304002'),
        ('http://player.vimeo.com/video/72304002', '72304002'),
        ('https://player.vimeo.com/video/72304002', '72304002'),
    )

    soundcloud_urls = (
        ('https://soundcloud.com/glassnote/mumford-sons-i-will-wait', '67129237'),
        ('https://soundcloud.com/matej-roman/jaromir-nohavica-karel-plihal-mikymauz', '7834701'),
        ('https://soundcloud.com/beny97/sets/jaromir-nohavica-prazska', '960591'),
        ('https://soundcloud.com/corbel-keep/norah-jones-come-away-with', '22485933'),
    )

    def setUp(self):
        from django.conf import settings as django_settings
        self.django_settings = django_settings

    def test_detect_bad_urls(self):
        for url in self.unknown_backend_urls:
            self.assertRaises(UnknownBackendException, detect_backend, url)

    def test_detect_youtube(self):
        for url in self.youtube_urls:
            backend = detect_backend(url[0])
            self.assertIsInstance(backend, YoutubeBackend)

    def test_detect_vimeo(self):
        for url in self.vimeo_urls:
            backend = detect_backend(url[0])
            self.assertIsInstance(backend, VimeoBackend)

    def test_detect_soundcloud(self):
        for url in self.soundcloud_urls:
            backend = detect_backend(url[0])
            self.assertIsInstance(backend, SoundCloudBackend)

    def test_code_youtube(self):
        for url in self.youtube_urls:
            backend = YoutubeBackend(url[0])
            code = backend.get_code()
            self.assertEqual(code, url[1])

    def test_code_vimeo(self):
        for url in self.vimeo_urls:
            backend = VimeoBackend(url[0])
            code = backend.get_code()
            self.assertEqual(code, url[1])

    def test_code_soundcloud(self):
        for url in self.soundcloud_urls:
            backend = SoundCloudBackend(url[0])
            code = backend.get_code()
            self.assertEqual(code, url[1])

    def test_vimeo_get_info_exception(self):
        self.assertRaises(VideoDoesntExistException, VimeoBackend,
                           'http://vimeo.com/123')

    def test_youtube_keyerror(self):
        """ Test for issue #7 """
        self.assertRaises(UnknownIdException, YoutubeBackend,
                          'http://youtube.com/watch?id=5')

