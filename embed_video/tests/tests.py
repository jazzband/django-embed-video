import os

from unittest import main, TestCase

from django.http import HttpRequest
from django.template.base import Template
from django.template.context import RequestContext

from ..base import detect_backend, YoutubeBackend, VimeoBackend, \
        SoundCloundBackend

os.environ['DJANGO_SETTINGS_MODULE'] = 'embed_video.tests.django_settings'


class EmbedVideoTestCase(TestCase):
    youtube_urls = (
        ('http://www.youtube.com/watch?v=jsrRJyHBvzw', 'jsrRJyHBvzw'),
        ('http://youtube.com/watch?v=jsrRJyHBvzw', 'jsrRJyHBvzw'),
        ('http://youtu.be/jsrRJyHBvzw', 'jsrRJyHBvzw'),
        ('http://www.youtube.com/watch?v=iwGFalTRHDA&feature=related', 'iwGFalTRHDA'),
        ('http://youtu.be/n17B_uFF4cA', 'n17B_uFF4cA'),
        ('http://www.youtube.com/watch?v=t-ZRX8984sc', 't-ZRX8984sc'),
        ('http://youtu.be/t-ZRX8984sc', 't-ZRX8984sc'),
    )

    vimeo_urls = (
        ('http://vimeo.com/66577491', '66577491'),
        ('http://www.vimeo.com/66577491', '66577491'),
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

    def _grc(self):
        return RequestContext(HttpRequest())

    def test_embed(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' as ytb %}
                {{ ytb|embed:'large' }}
            {% endvideo %}
        """)
        rendered = u'<iframe width="960" height="720" src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" frameborder="0" allowfullscreen></iframe>'

        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_embed_user_size(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' as ytb %}
                {{ ytb|embed:'800x800' }}
            {% endvideo %}
        """)
        rendered = u'<iframe width="800" height="800" src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" frameborder="0" allowfullscreen></iframe>'

        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_tag_youtube(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' as ytb %}
                {{ ytb.url }}
            {% endvideo %}
        """)
        rendered = 'http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque'

        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_tag_vimeo(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'https://vimeo.com/66577491' as vimeo %}
                {{ vimeo.url }}
            {% endvideo %}
        """)
        rendered = 'http://player.vimeo.com/video/66577491'

        self.assertEqual(template.render(self._grc()).strip(), rendered)

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
            self.assertIsInstance(backend, SoundCloundBackend)

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
            backend = SoundCloundBackend(url[0])
            code = backend.get_code()
            self.assertEqual(code, url[1])


if __name__ == '__main__':
    main()
