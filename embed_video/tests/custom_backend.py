import re

from embed_video.backends import VideoBackend


class CustomBackend(VideoBackend):
    re_detect = re.compile(r'http://myvideo\.com/[0-9]+')
    re_code = re.compile(r'http://myvideo\.com/(?P<code>[0-9]+)')

    pattern_url = 'http://play.myvideo.com/c/%s/'
    pattern_thumbnail_url = 'http://thumb.myvideo.com/c/%s/'
