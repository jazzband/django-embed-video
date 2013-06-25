import re
import urlparse
import requests
import json

DETECT_YOUTUBE = re.compile(
    r'^(http(s)?://(www\.)?)?youtu(\.?)be(\.com)?.*', re.I
)
DETECT_VIMEO = re.compile(
    r'^(http(s)?://(www\.)?)?vimeo\.com.*', re.I
)
DETECT_SOUNDCLOUD = re.compile(
    r'^(http(s)?://(www\.)?)?soundcloud\.com.*', re.I
)


class UnknownBackendException(Exception):
    pass


class NoIdFound(Exception):
    pass


def detect_backend(url):
    if DETECT_YOUTUBE.match(url):
        return YoutubeBackend(url)
    elif DETECT_VIMEO.match(url):
        return VimeoBackend(url)
    elif DETECT_SOUNDCLOUD.match(url):
        return SoundCloundBackend(url)
    else:
        raise UnknownBackendException


class VideoBackend(object):
    def __init__(self, url):
        self._url = url

        self.code = self.get_code()
        self.url = self.get_url()
        self.thumbnail = self.get_thumbnail_url()

    def get_code(self):
        match = self.re_code.search(self._url)
        if match:
            return match.group('code')
        else:
            parse_data = urlparse.urlparse(self._url)
            try:
                return urlparse.parse_qs(parse_data.query)['v'][0]
            except KeyError:
                pass
            raise NoIdFound

    def get_url(self):
        return self.pattern_url % self.code

    def get_thumbnail_url(self):
        return self.pattern_thumbnail_url % self.code


class SoundCloundBackend(VideoBackend):
    base_url = 'http://soundcloud.com/oembed'

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

        super(SoundCloundBackend, self).__init__(url)

    def get_thumbnail_url(self):
        return self.response.get('thumbnail_url')

    def get_url(self):
        match = self.re_url.search(self.response.get('html'))
        return match.group('url')

    def get_code(self):
        match = self.re_code.search(self.response.get('html'))
        return match.group('code')


class YoutubeBackend(VideoBackend):
    re_code = re.compile(
        r'youtu(?:be\.com/watch\?v=|\.be/)(?P<code>[\w-]*)(&(amp;)?[\w\?=]*)?',
        re.I
    )
    pattern_url = 'http://www.youtube.com/embed/%s?wmode=opaque'
    pattern_thumbnail_url = 'http://img.youtube.com/vi/%s/hqdefault.jpg'


class VimeoBackend(VideoBackend):
    re_code = re.compile(r'vimeo\.com/(?P<code>[0-9]+)', re.I)
    pattern_url = 'http://player.vimeo.com/video/%s'

    def get_thumbnail_url(self):
        pass  # not implemented
