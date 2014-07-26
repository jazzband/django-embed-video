from unittest import TestCase

from embed_video.backends import detect_backend, UnknownBackendException, \
    VideoBackend


class BackendTestMixin(object):
    urls = []
    instance = None

    def test_detect(self):
        for url in self.urls:
            backend = detect_backend(url[0])
            self.assertIsInstance(backend, self.instance)

    def test_code(self):
        for url in self.urls:
            backend = self.instance(url[0])
            self.assertEqual(backend.code, url[1])


class VideoBackendTestCase(TestCase):
    unknown_backend_urls = (
        'http://myurl.com/?video=http://www.youtube.com/watch?v=jsrRJyHBvzw',
        'http://myurl.com/?video=www.youtube.com/watch?v=jsrRJyHBvzw',
        'http://youtube.com.myurl.com/watch?v=jsrRJyHBvzw',
        'http://vimeo.com.myurl.com/72304002',
    )

    def test_detect_bad_urls(self):
        for url in self.unknown_backend_urls:
            self.assertRaises(UnknownBackendException, detect_backend, url)

    def test_not_implemented_get_info(self):
        backend = VideoBackend('http://www.example.com')
        self.assertRaises(NotImplementedError, backend.get_info)
