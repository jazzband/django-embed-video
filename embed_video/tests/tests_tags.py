from unittest import TestCase
from django.test.client import RequestFactory
from mock import Mock

from django.template import TemplateSyntaxError
from django.http import HttpRequest
from django.template.base import Template
from django.template.context import RequestContext

from embed_video.templatetags.embed_video_tags import VideoNode


class EmbedVideoNodeTestCase(TestCase):
    def setUp(self):
        self.parser = Mock()
        self.token = Mock(methods=['split_contents'])

    @staticmethod
    def _grc():
        return RequestContext(HttpRequest())

    def test_embed(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' as ytb %}
                {% video ytb 'large' %}
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

    def test_direct_embed_tag(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video "http://www.youtube.com/watch?v=jsrRJyHBvzw" "large" %}
        """)
        rendered = u'<iframe width="960" height="720" src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" frameborder="0" allowfullscreen></iframe>'
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_user_size(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' as ytb %}
                {% video ytb '800x800' %}
            {% endvideo %}
        """)
        rendered = u'<iframe width="800" height="800" src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" frameborder="0" allowfullscreen></iframe>'
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_wrong_size(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' 'so x huge' %}
        """)
        self.assertRaises(TemplateSyntaxError, template.render, self._grc())

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
            {% video 'https://soundcloud.com/community/soundcloud-case-study-wildlife' as soundcloud %}
                {{ soundcloud.backend }}
            {% endvideo %}
        """)
        rendered = 'SoundCloudBackend'
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_syntax_error(self):
        self.token.split_contents.return_value = []
        self.assertRaises(TemplateSyntaxError, VideoNode, self.parser, self.token)

    def test_repr(self):
        self.token.split_contents.return_value = (
            'video', 'http://youtu.be/v/1234', 'as', 'myvideo'
        )
        self.parser.compile_filter.return_value = u'some_url'

        node = VideoNode(self.parser, self.token)
        self.assertEqual(str(node), '<VideoNode "some_url">')

    def test_videonode_iter(self):
        out = ['a', 'b', 'c', 'd']

        class FooNode(VideoNode):
            nodelist_file = out

            def __init__(self):
                pass

        node = FooNode()
        self.assertEqual(out, [x for x in node])

    def test_get_backend_secure(self):
        class SecureRequest(RequestFactory):
            is_secure = lambda x: True

        context = {'request': SecureRequest()}
        backend = VideoNode.get_backend('http://www.youtube.com/watch?v=jsrRJyHBvzw', context)
        self.assertTrue(backend.is_secure)

    def test_get_backend_insecure(self):
        class InsecureRequest(RequestFactory):
            is_secure = lambda x: False

        context = {'request': InsecureRequest()}
        backend = VideoNode.get_backend('http://www.youtube.com/watch?v=jsrRJyHBvzw', context)
        self.assertFalse(backend.is_secure)



