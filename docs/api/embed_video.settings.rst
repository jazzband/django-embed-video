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


.. setting:: EMBED_VIDEO_{BACKEND}_QUERY

EMBED_VIDEO_{BACKEND}_QUERY
---------------------------

Set default query dictionary for including in the embedded URL.  This is
backend-specific.  Substitute the actual name of the backend for {BACKEND}
(i.e. to set the default query for the YouTube backend, the setting name would
be ``EMBED_VIDEO_YOUTUBE_QUERY`` and for SoundCloud the name would be
``EMBED_VIDEO_SOUNDCLOUD_QUERY``).  

As an example, if you set the following::

    EMBED_VIDEO_YOUTUBE_QUERY = {
        'wmode': 'opaque',
        'rel': '0'
    }

All URLs for YouTube will include the query string ``?wmode=opaque&rel=0``.

The default value for EMBED_VIDEO_YOUTUBE_QUERY is ``{'wmode': 'opaque'}``.
None of the other backends have default values set.
