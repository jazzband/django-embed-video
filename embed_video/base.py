import re

DETECT_YOUTUBE = re.compile(
    '^(http(s)?://(www\.)?)?youtu(\.?)be(\.com)?.*', re.I
)
DETECT_VIMEO = re.compile('^(http(s)?://(www\.)?)?vimeo\.com.*', re.I)


class UnknownBackendException(Exception):
    pass


def detect_backend(url):
    if DETECT_YOUTUBE.match(url):
        return YoutubeBackend(url)
    elif DETECT_VIMEO.match(url):
        return VimeoBackend(url)
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

    def get_url(self):
        return self.pattern_url % self.code

    def get_thumbnail_url(self):
        return self.pattern_thumbnail_url % self.code


class YoutubeBackend(VideoBackend):
    re_code = re.compile(
        'youtu(?:be\.com/watch\?v=|\.be/)(?P<code>[\w-]*)(&(amp;)?[\w\?=]*)?',
        re.I
    )
    pattern_url = 'http://www.youtube.com/embed/%s?wmode=opaque'
    pattern_thumbnail_url = 'http://img.youtube.com/vi/%s/hqdefault.jpg'


class VimeoBackend(VideoBackend):
    re_code = re.compile('vimeo\.com/(?P<code>[0-9]+)', re.I)
    pattern_url = 'http://player.vimeo.com/video/%s'

    def get_thumbnail_url(self):
        pass  # not implemented
