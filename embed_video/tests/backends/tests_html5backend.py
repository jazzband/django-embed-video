from unittest import TestCase

from . import BackendTestMixin
from embed_video.backends import (Html5VideoBackend, UnknownIdException,
    Html5AudioBackend)


class Html5VideoBackendTestCase(BackendTestMixin, TestCase):
    urls = (
        ('http://example.com/test.mp4', None),
        ('https://example.com/test/foo123.mov', None),
        ('http://example.com/#/test.webm', None),
    )

    instance = Html5VideoBackend


class Html5AudioBackendTestCase(BackendTestMixin, TestCase):
    urls = (
        ('http://example.com/test.mp3', None),
        ('https://example.com/test/foo123.wav', None),
        ('http://example.com/#/test.webm', None),
    )

    instance = Html5AudioBackend
