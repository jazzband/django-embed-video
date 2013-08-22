Examples
==============================================

Template examples
##############################################

.. highlight:: html+django

First you have to load the `embed_video_tags` template tags in your template:

::

    {% load embed_video_tags %}

Simple embeding of video:

::

    {% video item.video as my_video %}
        {{ my_video|embed:'small' }}
    {% endvideo %}

Default sizes are ``tiny`` (420x315), ``small`` (480x360), ``medium`` (640x480),
``large`` (960x720) and ``huge`` (1280x960). You can set your own size:

::

    {{ my_video|embed:'800x600' }}

Usage of variables:

::

    {% video item.video as my_video %}
        URL: {{ my_video.url }}
        Thumbnail: {{ my_video.thumbnail }}
        Backend: {{ my_video.backend }}
    {% endvideo %}


There is a simplier way, if you don't need work with parameters as
``my_video.url`` or ``my_video.thumbnail`` and you want to use just ``embed``
tag.

::

    {{ 'http://www.youtube.com/watch?v=guXyvo2FfLs'|embed:'large' }}




Model examples
###############################################

.. highlight:: python

Using the EmbedVideoField provides you validation of URLs.

::

    from django.db import models
    from embed_video.fields import EmbedVideoField

    class Item(models.Model):
        video = EmbedVideoField()  # same like models.URLField()



Admin examples
###############################################

.. todo::

  Admin mixins are on TODO list. Be patient or send :doc:`pull request
  </development/contributing>` :).



Low level API examples
###############################################

You can get instance of :py:class:`~embed_video.backends.VideoBackend` in your
python code thanks to :py:func:`~embed_video.backends.detect_backend`:

::

  from embed_video.backends import detect_backend

  my_video = detect_backend('http://www.youtube.com/watch?v=H4tAOexHdR4')

