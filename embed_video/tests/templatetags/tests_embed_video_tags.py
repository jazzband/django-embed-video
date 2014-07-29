from unittest import TestCase, skip
from mock import Mock, patch
import re

from django.template import TemplateSyntaxError
from django.http import HttpRequest
from django.template.base import Template
from django.template.context import RequestContext
from django.test.client import RequestFactory
from testfixtures import log_capture

from embed_video.templatetags.embed_video_tags import VideoNode

URL_PATTERN = re.compile(r'src="?\'?([^"\'>]*)"')


class EmbedTestCase(TestCase):
    def assertRenderedTemplate(self, template_string, output, context=None):
        response = RequestContext(HttpRequest(), context)
        rendered_output = Template(template_string).render(response)
        self.assertEqual(rendered_output.strip(), output.strip())

    def test_embed(self):
        template = """
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' as ytb %}
                {% video ytb 'large' %}
            {% endvideo %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="960" height="720" '
            'src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" '
            'frameborder="0" allowfullscreen></iframe>'
        )

    def test_embed_invalid_url(self):
        template = """
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/edit?abcd=efgh' as ytb %}
                {{ ytb.url }}
            {% endvideo %}
        """
        self.assertRenderedTemplate(template, '')

    def test_embed_with_none_instance(self):
        template = """
            {% with None as my_video %}
            {% load embed_video_tags %}
            {% video my_video %}{% endwith %}
        """
        self.assertRenderedTemplate(template, '')

    def test_embed_empty_string(self):
        template = """
            {% load embed_video_tags %}
            {% video '' 'large' %}
        """
        self.assertRenderedTemplate(template, '')

    def test_direct_embed_tag(self):
        template = """
            {% load embed_video_tags %}
            {% video "http://www.youtube.com/watch?v=jsrRJyHBvzw" "large" %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="960" height="720" '
            'src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" '
            'frameborder="0" allowfullscreen></iframe>'
        )

    def test_direct_embed_tag_with_default_size(self):
        template = """
            {% load embed_video_tags %}
            {% video "http://www.youtube.com/watch?v=jsrRJyHBvzw" %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="480" height="360" '
            'src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" '
            'frameborder="0" allowfullscreen></iframe>'
        )

    def test_direct_embed_invalid_url(self):
        template = """
            {% load embed_video_tags %}
            {% video "https://soundcloud.com/xyz/foo" %}
        """
        self.assertRenderedTemplate(template, '')

    def test_user_size(self):
        template = """
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' as ytb %}
                {% video ytb '800x800' %}
            {% endvideo %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="800" height="800" '
            'src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" '
            'frameborder="0" allowfullscreen></iframe>'
        )

    def test_wrong_size(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' 'so x huge' %}
        """)
        request = RequestContext(HttpRequest())
        self.assertRaises(TemplateSyntaxError, template.render, request)

    def test_tag_youtube(self):
        template = """
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' as ytb %}
                {{ ytb.url }} {{ ytb.backend }}
            {% endvideo %}
        """
        self.assertRenderedTemplate(
            template,
            'http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque '
            'YoutubeBackend'
        )

    def test_tag_vimeo(self):
        template = """
            {% load embed_video_tags %}
            {% video 'https://vimeo.com/72304002' as vimeo %}
                {{ vimeo.url }} {{ vimeo.backend }} {{ vimeo.info.duration }}
            {% endvideo %}
        """
        self.assertRenderedTemplate(
            template, 'http://player.vimeo.com/video/72304002 VimeoBackend 176'
        )

    def test_tag_soundcloud(self):
        template = """
            {% load embed_video_tags %}
            {% video 'https://soundcloud.com/community/soundcloud-case-study-wildlife' as soundcloud %}
                {{ soundcloud.url }} {{ soundcloud.backend }}
            {% endvideo %}
        """
        self.assertRenderedTemplate(
            template,
            'https://w.soundcloud.com/player/?visual=true&amp;url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F82244706&amp;show_artwork=true '
            'SoundCloudBackend'
        )

    @patch('embed_video.backends.EMBED_VIDEO_TIMEOUT', 0.000001)
    @log_capture()
    def test_empty_if_timeout(self, logs):
        template = """
            {% load embed_video_tags %}
            {% video "http://vimeo.com/72304002" as my_video %}
                {{ my_video.thumbnail }}
            {% endvideo %}
        """

        self.assertRenderedTemplate(template, '')
        logs.check(
            ('requests.packages.urllib3.connectionpool', 'INFO', 'Starting new HTTP connection (1): vimeo.com'),
            ('embed_video.templatetags.embed_video_tags', 'ERROR', 'Timeout reached during rendering embed video (`http://vimeo.com/72304002`)')
        )

    def test_relative_size(self):
        template = """
            {% load embed_video_tags %}
            {% video "http://vimeo.com/72304002" "80%x30%" %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="80%" height="30%" '
            'src="http://player.vimeo.com/video/72304002" '
            'frameborder="0" allowfullscreen></iframe>'
        )

    def test_allow_spaces_in_size(self):
        template = """
            {% load embed_video_tags %}
            {% video "http://vimeo.com/72304002" "80% x 300" %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="80%" height="300" '
            'src="http://player.vimeo.com/video/72304002" '
            'frameborder="0" allowfullscreen></iframe>'
        )

    def test_embed_with_query(self):
        template = """
           {% load embed_video_tags %}
           {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' query="rel=1&wmode=transparent" as ytb %}
               {{ ytb.url }}
           {% endvideo %}
        """
        self.assertRenderedTemplate(
            template,
            'http://www.youtube.com/embed/jsrRJyHBvzw?wmode=transparent&rel=1'
        )

    def test_direct_embed_with_query(self):
        template = """
           {% load embed_video_tags %}
           {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' query="rel=1&wmode=transparent" %}
        """

        self.assertRenderedTemplate(
            template,
            '<iframe width="480" height="360" '
            'src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=transparent&rel=1" '
            'frameborder="0" allowfullscreen></iframe>'
        )

    def test_set_options(self):
        template = """
           {% load embed_video_tags %}
           {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' "300x200" is_secure=True query="rel=1" %}
       """
        self.assertRenderedTemplate(
            template,
            '<iframe width="300" height="200" '
            'src="https://www.youtube.com/embed/jsrRJyHBvzw?rel=1" '
            'frameborder="0" allowfullscreen></iframe>'
        )

    def test_size_as_variable(self):
        template = """
            {% load embed_video_tags %}
            {% with size="500x200" %}
                {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' size %}
            {% endwith %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="500" height="200" '
            'src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" '
            'frameborder="0" allowfullscreen></iframe>'
        )


class EmbedVideoNodeTestCase(TestCase):
    def setUp(self):
        self.parser = Mock()
        self.token = Mock(methods=['split_contents'])

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

