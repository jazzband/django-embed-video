"""
Django app for easy embeding YouTube and Vimeo videos and music from
SoundCloud.
"""

VERSION = (0, 11, 'dev')


def get_release():
    return '.'.join(str(i) for i in VERSION[:3])


def get_version():
    """
    Returns only digit parts of version.
    """
    return '.'.join(str(i) for i in VERSION[:2])


__version__ = get_release()
