import sys

if sys.version_info >= (3, 8):
    import importlib.metadata as metadata
else:
    import importlib_metadata as metadata

__version__ = metadata.version("django-embed-video")
