import re
import sys
import json
import requests

if sys.version_info.major == 3:
    import urllib.parse as urlparse
else:
    import urlparse

from django.http import QueryDict
from django.template.loader import render_to_string
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe

from .utils import import_by_path
from .settings import EMBED_VIDEO_BACKENDS, EMBED_VIDEO_TIMEOUT, \
    EMBED_VIDEO_YOUTUBE_DEFAULT_QUERY


class EmbedVideoException(Exception):
    """ Parental class for all embed_video exceptions """
    pass


class VideoDoesntExistException(EmbedVideoException):
    """ Exception thrown if video doesn't exist """
    pass


class UnknownBackendException(EmbedVideoException):
    """ Exception thrown if video backend is not recognized. """
    pass


class UnknownIdException(VideoDoesntExistException):
    """
    Exception thrown if backend is detected, but video ID cannot be parsed.
    """
    pass


def detect_backend(url):
    """
    Detect the right backend for given URL.

    Goes over backends in ``settings.EMBED_VIDEO_BACKENDS``,
    calls :py:func:`~VideoBackend.is_valid` and returns backend instance.

    :param url: URL which is passed to `is_valid` methods of VideoBackends.
    :type url: str

    :return: Returns recognized VideoBackend
    :rtype: VideoBackend
    """

    for backend_name in EMBED_VIDEO_BACKENDS:
        backend = import_by_path(backend_name)
        if backend.is_valid(url):
            return backend(url)

    raise UnknownBackendException


class VideoBackend(object):
    """
    Base class used as parental class for backends.


    Backend variables:

    .. autosummary::

        url
        code
        thumbnail
        query
        info
        is_secure
        protocol
        template_name


    .. code-block:: python

        class MyBackend(VideoBackend):
            ...

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

    :type: str
    """

    pattern_thumbnail_url = None
    """
    Pattern in which the code is inserted to get thumbnail url.

    Example: ``http://static.myvideo.com/thumbs/%s``

    :type: str
    """

    allow_https = True
    """
    Sets if HTTPS version allowed for specific backend.

    :type: bool
    """

    template_name = 'embed_video/embed_code.html'
    """
    Name of embed code template used by :py:meth:`get_embed_code`.

    Passed template variables: ``{{ backend }}`` (instance of VideoBackend),
    ``{{ width }}``, ``{{ height }}``

    :type: str
    """

    default_query = ''
    """
    Default query string or `QueryDict` appended to url

    :type: str
    """

    is_secure = False
    """
    Decides if secured protocol (HTTPS) is used.

    :type: bool
    """

    def __init__(self, url):
        """
        First it tries to load data from cache and if it don't succeed, run
        :py:meth:`init` and then save it to cache.

        :type url: str
        """
        self.backend = self.__class__.__name__
        self._url = url
        self.query = QueryDict(self.default_query, mutable=True)

    @property
    def code(self):
        """
        Code of video.
        """
        return self.get_code()

    @property
    def url(self):
        """
        URL of video.
        """
        return self.get_url()

    @property
    def protocol(self):
        """
        Protocol used to generate URL.
        """
        return 'https' if self.allow_https and self.is_secure else 'http'

    @property
    def thumbnail(self):
        """
        URL of video thumbnail.
        """
        return self.get_thumbnail_url()

    @property
    def info(self):
        """
        Additional information about video. Not implemented in all backends.
        """
        return self.get_info()

    @property
    def query(self):
        """
        String transformed to QueryDict appended to url.
        """
        return self._query

    @query.setter
    def query(self, value):
        """
        :type value: QueryDict | str
        """
        self._query = value \
            if isinstance(value, QueryDict) \
            else QueryDict(value, mutable=True)

    @classmethod
    def is_valid(cls, url):
        """
        Class method to control if passed url is valid for current backend. By
        default it is done by :py:data:`re_detect` regex.

        :type url: str
        """
        return True if cls.re_detect.match(url) else False

    def get_code(self):
        """
        Returns video code matched from given url by :py:data:`re_code`.

        :rtype: str
        """
        match = self.re_code.search(self._url)
        if match:
            return match.group('code')

    def get_url(self):
        """
        Returns URL folded from :py:data:`pattern_url` and parsed code.
        """
        url = self.pattern_url.format(code=self.code, protocol=self.protocol)
        url += '?' + self.query.urlencode() if self.query else ''
        return mark_safe(url)

    def get_thumbnail_url(self):
        """
        Returns thumbnail URL folded from :py:data:`pattern_thumbnail_url` and
        parsed code.

        :rtype: str
        """
        return self.pattern_thumbnail_url.format(code=self.code,
                                                 protocol=self.protocol)

    def get_embed_code(self, width, height):
        """
        Returns embed code rendered from template :py:data:`template_name`.

        :type width: int | str
        :type height: int | str
        :rtype: str
        """
        return render_to_string(self.template_name, {
            'backend': self,
            'width': width,
            'height': height,
        })

    def get_info(self):
        """
        :rtype: dict
        """
        raise NotImplementedError

    def set_options(self, options):
        """
        :type options: dict
        """
        for key in options:
            setattr(self, key, options[key])


class YoutubeBackend(VideoBackend):
    """
    Backend for YouTube URLs.
    """
    re_detect = re.compile(
        r'^(http(s)?://)?(www\.|m\.)?youtu(\.?)be(\.com)?/.*', re.I
    )

    re_code = re.compile(
        r'''youtu(\.?)be(\.com)?/  # match youtube's domains
            (\#/)? # for mobile urls
            (embed/)?  # match the embed url syntax
            (v/)?
            (watch\?v=)?  # match the youtube page url
            (ytscreeningroom\?v=)?
            (feeds/api/videos/)?
            (user\S*[^\w\-\s])?
            (?P<code>[\w\-]{11})[a-z0-9;:@?&%=+/\$_.-]*  # match and extract
        ''',
        re.I | re.X
    )

    pattern_url = '{protocol}://www.youtube.com/embed/{code}'
    pattern_thumbnail_url = '{protocol}://img.youtube.com/vi/{code}/{resolution}'
    default_query = EMBED_VIDEO_YOUTUBE_DEFAULT_QUERY
    resolutions = [
        'maxresdefault.jpg',
        'sddefault.jpg',
        'hqdefault.jpg',
        'mqdefault.jpg',
    ]

    def get_code(self):
        code = super(YoutubeBackend, self).get_code()

        if not code:
            parsed_url = urlparse.urlparse(self._url)
            parsed_qs = urlparse.parse_qs(parsed_url.query)

            if 'v' in parsed_qs:
                code = parsed_qs['v'][0]
            elif 'video_id' in parsed_qs:
                code = parsed_qs['video_id'][0]
            else:
                raise UnknownIdException('Cannot get ID from `{0}`'.format(self._url))

        return code

    def get_thumbnail_url(self):
        """
        Returns thumbnail URL folded from :py:data:`pattern_thumbnail_url` and
        parsed code.

        :rtype: str
        """
        for resolution in self.resolutions:
            temp_thumbnail_url = self.pattern_thumbnail_url.format(
                code=self.code, protocol=self.protocol, resolution=resolution)
            if int(requests.head(temp_thumbnail_url).status_code) < 400:
                return temp_thumbnail_url
        return None


class VimeoBackend(VideoBackend):
    """
    Backend for Vimeo URLs.
    """
    re_detect = re.compile(
        r'^((http(s)?:)?//)?(www\.)?(player\.)?vimeo\.com/.*', re.I
    )
    re_code = re.compile(r'''vimeo\.com/(video/)?(channels/(.*/)?)?(?P<code>[0-9]+)''', re.I)
    pattern_url = '{protocol}://player.vimeo.com/video/{code}'
    pattern_info = '{protocol}://vimeo.com/api/v2/video/{code}.json'

    def get_info(self):
        try:
            response = requests.get(
                self.pattern_info.format(code=self.code, protocol=self.protocol),
                timeout=EMBED_VIDEO_TIMEOUT
            )
            return json.loads(response.text)[0]
        except ValueError:
            raise VideoDoesntExistException()

    def get_thumbnail_url(self):
        return self.info.get('thumbnail_large')


class SoundCloudBackend(VideoBackend):
    """
    Backend for SoundCloud URLs.
    """
    base_url = '{protocol}://soundcloud.com/oembed'

    re_detect = re.compile(r'^(http(s)?://(www\.)?)?soundcloud\.com/.*', re.I)
    re_code = re.compile(r'src=".*%2F(?P<code>\d+)&show_artwork.*"', re.I)
    re_url = re.compile(r'src="(?P<url>.*?)"', re.I)

    @cached_property
    def width(self):
        """
        :rtype: str
        """
        return self.info.get('width')

    @cached_property
    def height(self):
        """
        :rtype: str
        """
        return self.info.get('height')

    def get_info(self):
        params = {
            'format': 'json',
            'url': self._url,
        }
        r = requests.get(self.base_url.format(protocol=self.protocol),
                         params=params,
                         timeout=EMBED_VIDEO_TIMEOUT)

        if r.status_code != 200:
            raise VideoDoesntExistException(
                'SoundCloud returned status code `{0}`.'.format(r.status_code)
            )

        return json.loads(r.text)

    def get_thumbnail_url(self):
        return self.info.get('thumbnail_url')

    def get_url(self):
        match = self.re_url.search(self.info.get('html'))
        return match.group('url')

    def get_code(self):
        match = self.re_code.search(self.info.get('html'))
        return match.group('code')

    def get_embed_code(self, width, height):
        return super(SoundCloudBackend, self). \
            get_embed_code(width=width, height=height)
