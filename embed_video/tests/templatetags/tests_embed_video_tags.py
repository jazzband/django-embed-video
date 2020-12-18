import re
import urllib.parse as urlparse
from unittest import TestCase
from unittest.mock import Mock, patch

from django.http import HttpRequest
from django.template import TemplateSyntaxError
from django.template.base import Template
from django.template.context import RequestContext
from django.test.client import RequestFactory

from embed_video.templatetags.embed_video_tags import VideoNode

URL_PATTERN = re.compile(r'src="?\'?([^"\'>]*)"')


class EmbedTestCase(TestCase):
    def render_template(self, template_string, context=None):
        response = RequestContext(HttpRequest(), context)
        return Template(template_string).render(response).strip()

    def assertRenderedTemplate(self, template_string, output, context=None):
        rendered_output = self.render_template(template_string, context=context)
        self.assertEqual(rendered_output, output.strip())

    def url_dict(self, url):
        """
        Parse the URL into a format suitable for comparison, ignoring the query
        parameter order.
        """

        parsed = urlparse.urlparse(url)
        query = urlparse.parse_qs(parsed.query)

        return {
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "path": parsed.path,
            "params": parsed.params,
            "query": query,
            "fragment": parsed.fragment,
        }

    def assertUrlEqual(self, actual, expected, msg=None):
        """Assert two URLs are equal, ignoring the query parameter order."""
        actual_dict = self.url_dict(actual)
        expected_dict = self.url_dict(expected)

        self.assertEqual(actual_dict, expected_dict, msg=msg)

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
            'src="https://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" '
            'loading="lazy" frameborder="0" allowfullscreen></iframe>',
        )

    def test_embed_invalid_url(self):
        template = """
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/edit?abcd=efgh' as ytb %}
                {{ ytb.url }}
            {% endvideo %}
        """
        self.assertRenderedTemplate(template, "")

    def test_embed_with_none_instance(self):
        template = """
            {% with None as my_video %}
            {% load embed_video_tags %}
            {% video my_video %}{% endwith %}
        """
        self.assertRenderedTemplate(template, "")

    def test_embed_empty_string(self):
        template = """
            {% load embed_video_tags %}
            {% video '' 'large' %}
        """
        self.assertRenderedTemplate(template, "")

    def test_direct_embed_tag(self):
        template = """
            {% load embed_video_tags %}
            {% video "http://www.youtube.com/watch?v=jsrRJyHBvzw" "large" %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="960" height="720" '
            'src="https://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" '
            'loading="lazy" frameborder="0" allowfullscreen></iframe>',
        )

    def test_direct_embed_tag_with_default_size(self):
        template = """
            {% load embed_video_tags %}
            {% video "http://www.youtube.com/watch?v=jsrRJyHBvzw" %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="480" height="360" '
            'src="https://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" '
            'loading="lazy" frameborder="0" allowfullscreen></iframe>',
        )

    def test_direct_embed_invalid_url(self):
        template = """
            {% load embed_video_tags %}
            {% video "https://soundcloud.com/xyz/foo" %}
        """
        self.assertRenderedTemplate(template, "")

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
            'src="https://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" '
            'loading="lazy" frameborder="0" allowfullscreen></iframe>',
        )

    def test_wrong_size(self):
        template = Template(
            """
            {% load embed_video_tags %}
            {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' 'so x huge' %}
        """
        )
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
            "https://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque " "YoutubeBackend",
        )

    def test_tag_vimeo(self):
        template = """
            {% load embed_video_tags %}
            {% video 'https://vimeo.com/72304002' as vimeo %}
                {{ vimeo.url }} {{ vimeo.backend }} {{ vimeo.info.duration }}
            {% endvideo %}
        """
        self.assertRenderedTemplate(
            template, "https://player.vimeo.com/video/72304002 VimeoBackend 176"
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
            "https://w.soundcloud.com/player/?visual=true&amp;url=https%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F82244706&amp;show_artwork=true "
            "SoundCloudBackend",
        )

    @patch("embed_video.backends.EMBED_VIDEO_TIMEOUT", 0.000001)
    @patch("urllib3.connectionpool.log")
    @patch("embed_video.templatetags.embed_video_tags.logger")
    def test_empty_if_timeout(self, embed_video_logger, urllib_logger):
        template = """
            {% load embed_video_tags %}
            {% video "http://vimeo.com/72304002" as my_video %}
                {{ my_video.thumbnail }}
            {% endvideo %}
        """

        self.assertRenderedTemplate(template, "")

        urllib_logger.debug.assert_called_with(
            "Starting new HTTPS connection (%d): %s:%s", 1, "vimeo.com", 443
        )

        embed_video_logger.exception.assert_called_with(
            "Timeout reached during rendering embed video (`http://vimeo.com/72304002`)"
        )

    def test_relative_size(self):
        template = """
            {% load embed_video_tags %}
            {% video "http://vimeo.com/72304002" "80%x30%" %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="80%" height="30%" '
            'src="https://player.vimeo.com/video/72304002" '
            'loading="lazy" frameborder="0" allowfullscreen></iframe>',
        )

    def test_allow_spaces_in_size(self):
        template = """
            {% load embed_video_tags %}
            {% video "http://vimeo.com/72304002" "80% x 300" %}
        """
        self.assertRenderedTemplate(
            template,
            '<iframe width="80%" height="300" '
            'src="https://player.vimeo.com/video/72304002" '
            'loading="lazy" frameborder="0" allowfullscreen></iframe>',
        )

    def test_embed_with_query(self):
        template = """
           {% load embed_video_tags %}
           {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' query="rel=1&wmode=transparent" as ytb %}
               {{ ytb.url }}
           {% endvideo %}
        """

        output = self.render_template(template)
        self.assertUrlEqual(
            output, "https://www.youtube.com/embed/jsrRJyHBvzw?rel=1&wmode=transparent"
        )

    def test_direct_embed_with_query(self):
        template = """
           {% load embed_video_tags %}
           {% video 'http://www.youtube.com/watch?v=jsrRJyHBvzw' query="rel=1&wmode=transparent" %}
        """

        output = self.render_template(template)

        # The order of query parameters in the URL might change between Python
        # versions. Compare the URL and the outer part separately.

        url_pattern = re.compile(r'http[^"]+')
        url = url_pattern.search(output).group(0)

        self.assertUrlEqual(
            url, "https://www.youtube.com/embed/jsrRJyHBvzw?rel=1&wmode=transparent"
        )

        output_without_url = url_pattern.sub("URL", output)

        self.assertEqual(
            output_without_url,
            '<iframe width="480" height="360" '
            'src="URL" '
            'loading="lazy" frameborder="0" allowfullscreen></iframe>',
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
            'loading="lazy" frameborder="0" allowfullscreen></iframe>',
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
            'src="https://www.youtube.com/embed/jsrRJyHBvzw?wmode=opaque" '
            'loading="lazy" frameborder="0" allowfullscreen></iframe>',
        )


class EmbedVideoNodeTestCase(TestCase):
    def setUp(self):
        self.parser = Mock()
        self.token = Mock(methods=["split_contents"])

    def test_repr(self):
        self.token.split_contents.return_value = (
            "video",
            "http://youtu.be/v/1234",
            "as",
            "myvideo",
        )
        self.parser.compile_filter.return_value = "some_url"

        node = VideoNode(self.parser, self.token)
        self.assertEqual(str(node), '<VideoNode "some_url">')

    def test_videonode_iter(self):
        out = ["a", "b", "c", "d"]

        class FooNode(VideoNode):
            nodelist_file = out

            def __init__(self):
                pass

        node = FooNode()
        self.assertEqual(out, [x for x in node])

    def test_get_backend_secure(self):
        class SecureRequest(RequestFactory):
            is_secure = lambda x: True

        context = {"request": SecureRequest()}
        backend = VideoNode.get_backend(
            "http://www.youtube.com/watch?v=jsrRJyHBvzw", context
        )
        self.assertTrue(backend.is_secure)

    def test_get_backend_insecure(self):
        class InsecureRequest(RequestFactory):
            is_secure = lambda x: False

        context = {"request": InsecureRequest()}
        backend = VideoNode.get_backend(
            "http://www.youtube.com/watch?v=jsrRJyHBvzw", context
        )
        self.assertFalse(backend.is_secure)
