Examples
========

Template examples
#################

.. highlight:: html+django

First you have to load the ``embed_video_tags`` template tags in your template:

::

    {% load embed_video_tags %}

Embedding of video:

::

    {# you can just embed #}
    {% video item.video 'small' %}

    {# or use variables (with embedding, too) #}
    {% video item.video as my_video %}
        URL: {{ my_video.url }}
        Thumbnail: {{ my_video.thumbnail }}
        Backend: {{ my_video.backend }}
        {% video my_video 'small' %}
    {% endvideo %}


Default sizes are ``tiny`` (420x315), ``small`` (480x360), ``medium`` (640x480),
``large`` (960x720) and ``huge`` (1280x960). You can set your own size:

::

    {% video my_video '800x600' %}

.. versionadded:: 0.7

    This usage has been added in version 0.7.

.. versionadded:: 0.9

  And use relative percentual size:

  ::

      {% video my_video '100% x 50%' %}


Some backends (e.g. YouTube) allow configuration of the embedding via passing
query parameters.  To specify the parameters:

::

    {% video item.video 'small' rel=0 %}

    {% video item.video 'small' start=2 stop=5 repeat=1 %}

    {% video item.video rel=0 as my_video %}
        URL: {{ my_video.url }}
        Thumbnail: {{ my_video.thumbnail }}
        Backend: {{ my_video.backend }}
        {% video my_video 'small' %}
    {% endvideo %}

Parameters may also be template variables:

::

    {% video item.video 'small' start=item.start stop=item.stop repeat=item.repeat %}


.. tip:: 

  You can provide default values for the query string that's included in the
  embedded URL by updating your Django settings file.


.. tip::

  We recommend to use `sorl-thumbnail
  <http://sorl-thumbnail.readthedocs.org/en/latest/>`_ to `change
  <http://sorl-thumbnail.readthedocs.org/en/latest/examples.html#template-examples>`_
  thumbnail size.

.. tip::

  To speed up your pages, consider `template fragment caching
  <https://docs.djangoproject.com/en/dev/topics/cache/#template-fragment-caching>`_.

.. tip::

    You can overwrite default template of embed code located in
    ``templates/embed_video/embed_code.html`` or set own file for custom
    backend (:py:data:`~embed_video.backends.VideoBackend.template_name`).

    .. versionadded:: 0.9
    
        ``template_name`` has been added in version 0.9.


Model examples
##############

.. highlight:: python

Using the ``EmbedVideoField`` provides you validation of URLs.

::

    from django.db import models
    from embed_video.fields import EmbedVideoField

    class Item(models.Model):
        video = EmbedVideoField()  # same like models.URLField()



Admin mixin examples
####################

Use ``AdminVideoMixin`` in ``admin.py``.

::

    from django.contrib import admin
    from embed_video.admin import AdminVideoMixin
    from .models import MyModel

    class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
        pass

    admin.site.register(MyModel, MyModelAdmin)




Custom backends
###############

If you have specific needs and default backends don't suits you, you can write
your custom backend.

``my_project/my_app/backends.py``::

  from embed_video.backends import VideoBackend

  class CustomBackend(VideoBackend):
      re_detect = re.compile(r'http://myvideo\.com/[0-9]+')
      re_code = re.compile(r'http://myvideo\.com/(?P<code>[0-9]+)')

      allow_https = False
      pattern_url = '{protocol}://play.myvideo.com/c/{code}/'
      pattern_thumbnail_url = '{protocol}://thumb.myvideo.com/c/{code}/'

      template_name = 'embed_video/custombackend_embed_code.html'  # added in v0.9

You can also overwrite :py:class:`~embed_video.backends.VideoBackend` methods,
if using regular expressions isn't well enough.

``my_project/my_project/settings.py``::

  EMBED_VIDEO_BACKENDS = (
      'embed_video.backends.YoutubeBackend',
      'embed_video.backends.VimeoBackend',
      'embed_video.backends.SoundCloudBackend',
      'my_app.backends.CustomBackend',
  )



Low level API examples
######################

You can get instance of :py:class:`~embed_video.backends.VideoBackend` in your
python code thanks to :py:func:`~embed_video.backends.detect_backend`:

::

  from embed_video.backends import detect_backend

  my_video = detect_backend('http://www.youtube.com/watch?v=H4tAOexHdR4')

