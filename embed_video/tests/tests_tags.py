from unittest import TestCase
from mock import Mock, patch
import re

try:
    # Python <= 2.7
    import urlparse
except ImportError:
    # Python 3
    import urllib.parse as urlparse

from django.template import TemplateSyntaxError
from django.http import HttpRequest
from django.template.base import Template
from django.template.context import RequestContext
from django.test.utils import override_settings
from django.test.client import RequestFactory
from testfixtures import LogCapture

from embed_video.templatetags.embed_video_tags import VideoNode

URL_PATTERN = re.compile(r'src="?\'?([^"\'>]*)"')


class EmbedVideoNodeTestCase(TestCase):
    def setUp(self):
        self.parser = Mock()
        self.token = Mock(methods=['split_contents'])

    @staticmethod
    def _grc(context=None):
        return RequestContext(HttpRequest(), context)

    def test_embed(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' as ytb %}
                {% video ytb 'large' %}
            {% endvideo %}
        """)
        rendered = u'''<iframe width="960" height="720" src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque"
        frameborder="0" allowfullscreen></iframe>'''
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_direct_embed(self):
        template = Template("""
            {% load embed_video_tags %}
            {{ 'http://www.youtube.com/watch?v=jsrRJyHBvzw'|embed:'large' }}
        """)
        rendered = u'''<iframe width="960" height="720" src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque"
        frameborder="0" allowfullscreen></iframe>'''
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_direct_embed_tag(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video "http://www.youtube.com/watch?v=jsrRJyHBvzw" "large" %}
        """)
        rendered = u'''<iframe width="960" height="720" src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque"
        frameborder="0" allowfullscreen></iframe>'''
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_direct_embed_tag_with_default_size(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video "http://www.youtube.com/watch?v=jsrRJyHBvzw" %}
        """)
        rendered = u'''<iframe width="480" height="360" src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque"
        frameborder="0" allowfullscreen></iframe>'''
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_user_size(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' as ytb %}
                {% video ytb '800x800' %}
            {% endvideo %}
        """)
        rendered = u'''<iframe width="800" height="800" src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque"
        frameborder="0" allowfullscreen></iframe>'''
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

    def test_tag_youtube_invalid_url(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/edit?abcd=efgh' as ytb %}
                {{ ytb.url }}
            {% endvideo %}
        """)
        self.assertEqual(template.render(self._grc()).strip(), '')

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

    def test_no_video_provided(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video '' 'large' %}
        """)
        self.assertEqual(template.render(self._grc()).strip(), '')

    @patch('embed_video.backends.EMBED_VIDEO_TIMEOUT', 0.000001)
    def test_empty_if_timeout(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video "http://vimeo.com/72304002" as my_video %}
                {{ my_video.thumbnail }}
            {% endvideo %}
        """)
        with LogCapture() as logs:
            self.assertEqual(template.render(self._grc()).strip(), '')
            log = logs.records[-1]
            self.assertEqual(log.name, 'embed_video.templatetags.embed_video_tags')
            self.assertEqual(log.msg, 'Timeout reached during rendering embed video (`http://vimeo.com/72304002`)')

    def test_relative_size(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video "http://vimeo.com/72304002" "80%x30%" %}
        """)
        rendered = '<iframe width="80%" height="30%" src="http://player.vimeo.com/video/72304002"' \
                   '\n        frameborder="0" allowfullscreen></iframe>'
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_allow_spaces_in_size(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video "http://vimeo.com/72304002" "80% x 300" %}
        """)
        rendered = '<iframe width="80%" height="300" src="http://player.vimeo.com/video/72304002"' \
                   '\n        frameborder="0" allowfullscreen></iframe>'
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_soundcloud_invalid_url(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video "https://soundcloud.com/xyz/foo" %}
        """)
        self.assertEqual(template.render(self._grc()).strip(), '')

    ##########################################################################
    # Tests for adding GET query via KEY=VALUE pairs
    ##########################################################################

    def _validate_GET_query(self, rendered, expected):
        # Use this functioon to test the KEY=VALUE optional arguments to the
        # templatetag because there's no guarantee that they will be appended
        # to the URL query string in a particular order.  By default the
        # YouTube backend adds wmode=opaque to the query string, so be sure to
        # include that in the expected querystring dict.
        url = URL_PATTERN.search(rendered).group(1)
        result = urlparse.urlparse(url)
        qs = urlparse.parse_qs(result[4])
        self.assertEqual(qs, expected)

    @override_settings(EMBED_VIDEO_YOUTUBE_QUERY={'rel': 0, 'stop': 5})
    def test_embed_with_query_settings_override(self):
        # Test KEY=VALUE argument with default values provided by settings
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' %}
        """)
        expected = {
            'rel': ['0'],
            'stop': ['5'],
        }
        rendered = template.render(self._grc())
        self._validate_GET_query(rendered, expected)

    def test_embed_with_query_var(self):
        # Test KEY=VALUE argument with the value resolving to a context
        # variable.
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' rel=show_related loop=5 %}
        """)
        expected = {
            'rel': ['0'],
            'loop': ['5'],
            'wmode': ['opaque']
        }
        context = {'show_related': 0}
        rendered = template.render(self._grc(context))
        self._validate_GET_query(rendered, expected)

    def test_embed_with_query_multiple(self):
        # Test multiple KEY=VALUE arguments
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' rel=0 loop=1 end=5 %}
        """)
        expected = {
            'rel': ['0'],
            'loop': ['1'],
            'end': ['5'],
            'wmode': ['opaque']
        }
        self._validate_GET_query(template.render(self._grc()), expected)

    def test_embed_with_query_multiple_list(self):
        # Test multiple KEY=VALUE arguments where the key is repeated multiple
        # times (this is valid in a URL query).
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' rel=0 loop=1 end=5 end=6 %}
        """)
        expected = {
            'rel': ['0'],
            'loop': ['1'],
            'end': ['5', '6'],
            'wmode': ['opaque']
        }
        self._validate_GET_query(template.render(self._grc()), expected)

    def test_tag_youtube_with_query(self):
        # Test KEY=VALUE arguments when used as a tag block.
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' rel=0 as ytb %}
                {{ ytb.url }}
            {% endvideo %}
        """)
        rendered = 'http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque&rel=0'
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_embed_with_query_rel(self):
        template = Template("""
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' rel=0 %}
        """)
        rendered = u'''<iframe width="480" height="360" src="http://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque&rel=0"
        frameborder="0" allowfullscreen></iframe>'''
        self.assertEqual(template.render(self._grc()).strip(), rendered)

    def test_none_variable_passed_to_tag(self):
        """
        Checks issue #24.
        """
        template = Template("""
            {% with None as my_video %}
            {% load embed_video_tags %}
            {% video my_video %}
            {% endwith %}
        """)
        self.assertEqual(template.render(self._grc()).strip(), '')

