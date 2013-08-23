"""
Django app for easy embeding YouTube and Vimeo videos and music from
SoundCloud.
"""

VERSION = (0, 5, 'dev')

__version__ = '.'.join(str(i) for i in VERSION[:3])


def get_version():
    """
    Returns only digit parts of version.
    """
    return '.'.join(str(i) for i in VERSION[:2])
