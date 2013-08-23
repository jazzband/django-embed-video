from unittest import TestCase
from mock import Mock

from django.template import TemplateSyntaxError
from django.http import HttpRequest
from django.template.base import Template
from django.template.context import RequestContext

from embed_video.backends import YoutubeBackend, SoundCloudBackend
from embed_video.templatetags.embed_video_tags import VideoNode, \
        _embed_get_size, _embed_get_params


class EmbedVideoNodeTestCase(TestCase):
    def setUp(self):
        self.parser = Mock()
        self.token = Mock(methods=['split_contents'])

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

    def test_direct_embed(self):
        template = Template("""
            {% load embed_video_tags %}
            {{ 'http://www.youtube.com/watch?v=jsrRJyHBvzw'|embed:'large' }}
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
            {% video 'https://vimeo.com/72304002' as vimeo %}
                {{ vimeo.url }}
            {% endvideo %}
        """)
        rendered = 'http://player.vimeo.com/video/72304002'

        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_tag_backend_variable_vimeo(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'https://vimeo.com/72304002' as vimeo %}
                {{ vimeo.backend }}
            {% endvideo %}
        """)
        rendered = 'VimeoBackend'
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_tag_backend_variable_youtube(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvz' as youtube %}
                {{ youtube.backend }}
            {% endvideo %}
        """)
        rendered = 'YoutubeBackend'
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_tag_backend_variable_soundcloud(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'https://soundcloud.com/glassnote/mumford-sons-i-will-wait' as soundcloud %}
                {{ soundcloud.backend }}
            {% endvideo %}
        """)
        rendered = 'SoundCloudBackend'
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_syntax_error(self):
        self.token.split_contents.return_value = []

        try:
            VideoNode(self.parser, self.token)
        except TemplateSyntaxError:
            assert True

    def test_repr(self):
        self.token.split_contents.return_value = (
            'video', 'http://youtu.be/v/1234', 'as', 'myvideo'
        )
        self.parser.compile_filter.return_value = u'some_url'

        node = VideoNode(self.parser, self.token)
        self.assertEqual(str(node), '<VideoNode "some_url">')

    def test_embed_get_params(self):
        url = 'http://youtu.be/jsrRJyHBvzw'
        backend = YoutubeBackend(url)
        params = _embed_get_params(backend, (3, 8))

        self.assertEqual('http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque', params['url'])
        self.assertEqual(3, params['width'])
        self.assertEqual(8, params['height'])

    def test_embed_get_params_soundcloud_height(self):
        url = 'https://soundcloud.com/glassnote/mumford-sons-i-will-wait'
        backend = SoundCloudBackend(url)
        params = _embed_get_params(backend, (1, 2))

        self.assertEqual(backend.height, params['height'])

    def test_videonode_iter(self):
        out = ['a', 'b', 'c', 'd']

        class FooNode(VideoNode):
            nodelist_file = out

            def __init__(self):
                pass

        node = FooNode()
        self.assertEqual(out, [x for x in node])


