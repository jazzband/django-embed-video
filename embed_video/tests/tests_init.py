from unittest import TestCase

import embed_video


class EmbedVideoTestCase(TestCase):
    def test_release(self):
        embed_video.VERSION = ('a', 'b', 'c', 'd')
        self.assertEqual('a.b.c-d', embed_video.get_release())

    def test_version(self):
        embed_video.VERSION = ('a', 'b', 'c', 'd')
        self.assertEqual('a.b.c', embed_video.get_version())
