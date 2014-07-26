Settings
========

.. setting:: EMBED_VIDEO_BACKENDS


EMBED_VIDEO_BACKENDS
--------------------

List of backends to use.

Default::

  EMBED_VIDEO_BACKENDS = (
      'embed_video.backends.YoutubeBackend',
      'embed_video.backends.VimeoBackend',
      'embed_video.backends.SoundCloudBackend',
  )


.. setting:: EMBED_VIDEO_TIMEOUT


EMBED_VIDEO_TIMEOUT
-------------------

Sets timeout for ``GET`` requests to remote servers.

Default: ``10``


.. setting:: EMBED_VIDEO_YOUTUBE_DEFAULT_QUERY


EMBED_VIDEO_YOUTUBE_DEFAULT_QUERY
---------------------------------

Sets default :py:attr:`~embed_video.backends.VideoBackend.query` appended
to YouTube url. Can be string or :py:class:`~django.http.QueryDict` instance.

Default: ``"wmode=opaque"``
