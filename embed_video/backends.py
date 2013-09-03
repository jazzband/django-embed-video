import re
import requests
import json

try:
    import urlparse  # py2
except:
    import urllib.parse as urlparse  # py3


from .utils import import_by_path
from .settings import EMBED_VIDEO_BACKENDS, EMBED_VIDEO_CACHE, \
                      EMBED_VIDEO_CACHE_TIMEOUT

cache = None
if EMBED_VIDEO_CACHE:
    from django.core.cache import cache


class VideoDoesntExistException(Exception):
    pass


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
        """
        First it tries to load data from cache and if it don't succeed, run
        :py:meth:`init` and then save it to cache.
        """
        if not self._restore_cache(url):
            self.init(url)
            self._set_cache(url)

    def _restore_cache(self, url):
        """
        Restore data from cache if cache is enabled.
        """
        if cache:
            data = cache.get(url)
            if data:
                self.__dict__ = data
                return True

    def _set_cache(self, url):
        """
        Set data to cache if cache is enabled.
        """
        if cache:
            cache.set(url, self.__dict__)

    def init(self, url):
        """
        Load all data (:py:meth:`get_code`, :py:meth:`get_url` etc.)
        """
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
        re.I | re.X
    )

    pattern_url = 'http://www.youtube.com/embed/%s?wmode=opaque'
    pattern_thumbnail_url = 'http://img.youtube.com/vi/%s/hqdefault.jpg'

    def get_code(self):
        code = super(YoutubeBackend, self).get_code()

        if not code:
            parse_data = urlparse.urlparse(self._url)

            try:
                code = urlparse.parse_qs(parse_data.query)['v'][0]
            except KeyError:
                raise UnknownIdException

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
    pattern_info = 'http://vimeo.com/api/v2/video/%s.json'

    info = None

    def init(self, url):
        self._url = url
        self.code = self.get_code()
        self.info = self.get_info()

        super(VimeoBackend, self).init(url)

    def get_info(self):
        try:
            response = requests.get(self.pattern_info % self.code)
            return json.loads(response.text)[0]
        except ValueError:
            raise VideoDoesntExistException()

    def get_thumbnail_url(self):
        return self.info['thumbnail_large']


class SoundCloudBackend(VideoBackend):
    """
    Backend for SoundCloud URLs.
    """
    base_url = 'http://soundcloud.com/oembed'

    re_detect = re.compile(r'^(http(s)?://(www\.)?)?soundcloud\.com/.*', re.I)
    re_code = re.compile(r'src=".*%2F(?P<code>\d+)&show_artwork.*"', re.I)
    re_url = re.compile(r'src="(?P<url>.*?)"', re.I)

    def init(self, url):
        params = {
            'format': 'json',
            'url': url,
        }

        r = requests.get(self.base_url, data=params)
        self.response = json.loads(r.text)

        self.width = self.response.get('width')
        self.height = self.response.get('height')

        super(SoundCloudBackend, self).init(url)

    def get_thumbnail_url(self):
        return self.response.get('thumbnail_url')

    def get_url(self):
        match = self.re_url.search(self.response.get('html'))
        return match.group('url')

    def get_code(self):
        match = self.re_code.search(self.response.get('html'))
        return match.group('code')
