import sys
import re
import requests
import json


if sys.version_info >= (3, ):
    import urllib.parse as urlparse
else:
    import urlparse


from .utils import import_by_path
from .settings import EMBED_VIDEO_BACKENDS


class UnknownBackendException(Exception):
    pass


class UnknownIdException(Exception):
    pass


def detect_backend(url):
    """
    Detect the right backend for given URL.
    """

    for backend_name in EMBED_VIDEO_BACKENDS:
        backend = import_by_path(backend_name)
        if backend.is_valid(url):
            return backend(url)

    raise UnknownBackendException


class VideoBackend(object):
    """
    Base backend, good to inherit.
    """

    re_code = None
    """
    Compiled regex (:py:func:`re.compile`) to search code in URL.

    Example: ``re.compile(r'myvideo\.com/\?code=(?P<code>\w+)')``
    """

    re_detect = None
    """
    Compilede regec (:py:func:`re.compile`) to detect, if input URL is valid
    for current backend.

    Example: ``re.compile(r'^http://myvideo\.com/.*')``
    """

    pattern_url = None
    """
    Pattern in which the code is inserted.

    Example: ``http://myvideo.com?code=%s``
    """

    pattern_thumbnail_url = None
    """
    Pattern in which the code is inserted to get thumbnail url.

    Example: ``http://static.myvideo.com/thumbs/%s``
    """

    def __init__(self, url):
        self._url = url

        self.backend = self.__class__.__name__
        self.code = self.get_code()
        self.url = self.get_url()
        self.thumbnail = self.get_thumbnail_url()

    @classmethod
    def is_valid(klass, url):
        """
        Class method to control if passed url is valid for current backend. By
        default it is done by :py:data:`re_detect` regex.
        """
        return True if klass.re_detect.match(url) else False

    def get_code(self):
        """
        Returns searched code from URL by :py:data:`re_code`.
        """
        match = self.re_code.search(self._url)
        if match:
            return match.group('code')

    def get_url(self):
        """
        Returns URL folded from :py:data:`pattern_url` and parsed code.
        """
        return self.pattern_url % self.code

    def get_thumbnail_url(self):
        """
        Returns thumbnail URL folded from :py:data:`pattern_thumbnail_url` and
        parsed code.
        """
        return self.pattern_thumbnail_url % self.code


class YoutubeBackend(VideoBackend):
    """
    Backend for YouTube URLs.
    """
    re_detect = re.compile(
        r'^(http(s)?://)?(www\.)?youtu(\.?)be(\.com)?/.*', re.I
    )

    re_code = re.compile(
        r'''youtu(\.?)be(\.com)?/  # match youtube's domains
            (embed/)?  # match the embed url syntax
            (v/)?
            (watch\?v=)?  # match the youtube page url
            (ytscreeningroom\?v=)?
            (feeds/api/videos/)?
            (user\S*[^\w\-\s])?
            (\S*[^\w\-\s])?
            (?P<code>[\w\-]{11})[a-z0-9;:@?&%=+/\$_.-]*  # match and extract
        ''',
        re.I|re.X
    )

    pattern_url = 'http://www.youtube.com/embed/%s?wmode=opaque'
    pattern_thumbnail_url = 'http://img.youtube.com/vi/%s/hqdefault.jpg'

    def get_code(self):
        code = super(YoutubeBackend, self).get_code()

        if not code:
            parse_data = urlparse.urlparse(self._url)
            code = urlparse.parse_qs(parse_data.query)['v'][0]

        return code


class VimeoBackend(VideoBackend):
    """
    Backend for Vimeo URLs.
    """
    re_detect = re.compile(
        r'^(http(s)?://)?(www\.)?(player\.)?vimeo\.com/.*', re.I
    )
    re_code = re.compile(r'''vimeo\.com/(video/)?(?P<code>[0-9]+)''', re.I)
    pattern_url = 'http://player.vimeo.com/video/%s'

    def get_thumbnail_url(self):
        pass  # not implemented


class SoundCloudBackend(VideoBackend):
    """
    Backend for SoundCloud URLs.
    """
    base_url = 'http://soundcloud.com/oembed'

    re_detect = re.compile(r'^(http(s)?://(www\.)?)?soundcloud\.com/.*', re.I)
    re_code = re.compile(r'src=".*%2F(?P<code>\d+)&show_artwork.*"', re.I)
    re_url = re.compile(r'src="(?P<url>.*?)"', re.I)

    def __init__(self, url):
        params = {
            'format': 'json',
            'url': url,
        }

        r = requests.get(self.base_url, data=params)
        self.response = json.loads(r.text)

        self.width = self.response.get('width')
        self.height = self.response.get('height')

        super(SoundCloudBackend, self).__init__(url)

    def get_thumbnail_url(self):
        return self.response.get('thumbnail_url')

    def get_url(self):
        match = self.re_url.search(self.response.get('html'))
        return match.group('url')

    def get_code(self):
        match = self.re_code.search(self.response.get('html'))
        return match.group('code')
