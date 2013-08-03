from unittest import TestCase
from mock import Mock

from django.template import TemplateSyntaxError

from ..templatetags.embed_video_tags import VideoNode


class EmbedVideoNodeTestCase(TestCase):
    def setUp(self):
        self.parser = Mock()
        self.token = Mock(methods=['split_contents'])

    def test_syntax_error(self):
        self.token.split_contents.return_value = []

        try:
            instance = VideoNode(self.parser, self.token)
        except TemplateSyntaxError:
            assert True

    def test_repr(self):
        self.token.split_contents.return_value = (
            'video', 'http://youtu.be/v/1234', 'as', 'myvideo'
        )
        self.parser.compile_filter.return_value = u'some_url'

        node = VideoNode(self.parser, self.token)
        self.assertEqual(str(node), '<VideoNode "some_url">')


