"""
Django app for easy embeding YouTube and Vimeo videos and music from
SoundCloud.
"""

VERSION = (1, 1, 2, 'stable')


def get_release():
    return '-'.join([get_version(), VERSION[-1]])


def get_version():
    """
    Returns only digit parts of version.
    """
    return '.'.join(str(i) for i in VERSION[:3])


__version__ = get_release()
