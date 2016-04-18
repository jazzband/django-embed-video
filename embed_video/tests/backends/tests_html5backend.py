from unittest import TestCase

from . import BackendTestMixin
from embed_video import backends


class HTML5BackendTestCase(TestCase):
    def test_url(self):
        url = 'https://collab-project.github.io/videojs-wavesurfer/examples/media/heres_johnny.wav'
        backend = backends.detect_backend(url)
        self.assertEqual(backend.get_url(), url)


class Html5VideoBackendTestCase(BackendTestMixin, TestCase):
    urls = (
        ('http://www.quirksmode.org/html5/videos/big_buck_bunny.mp4', None),
        ('https://collab-project.github.io/videojs-wavesurfer/examples/media/example.mp4', None),
    )

    instance = backends.Html5VideoBackend


class Html5AudioBackendTestCase(BackendTestMixin, TestCase):
    urls = (
        ('https://collab-project.github.io/videojs-wavesurfer/examples/media/heres_johnny.wav', None),
    )

    instance = backends.Html5AudioBackend
