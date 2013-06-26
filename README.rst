django-embed-video
==================

Django app for easy embeding YouTube and Vimeo videos and music from SoundCloud.

.. image:: https://travis-ci.org/yetty/django-embed-video.png?branch=master


Installation
************

::

    pip install django-embed-video


or from sources

::

    pip install git+https://github.com/yetty/django-embed-video.git


Add ``embed_video`` to ``INSTALLED_APPS`` in your Django settings.


Examples
********

Template examples
-----------------

First you have to load the `embed_video_tags` template tags in your template:

::

    {% load embed_video_tags %}

Simple embeding of video:

::

    {% video item.video as video %}
        {{ video|embed:'small' }}
    {% endvideo %}

Default sizes are ``tiny`` (420x315), ``small`` (480x360), ``medium`` (640x480),
``large`` (960x720) and ``huge`` (1280x960). You can set your own size:

::

    {{ video|embed:'800x600' }}

Usage of variables:

::

    {% video item.video as video %}
        URL: {{ video.url }}
        Thumbnail: {{ video.thumbnail }}
    {% endvideo %}


Model examples
---------------

Using the EmbedVideoField you provide validation of correct URL.

::

    from django.db import models
    from embed_video.fields import EmbedVideoField

    class Item(models.Model):
        video = EmbedVideoField()  # same like models.URLField()


TODO
*****

- provide AdminEmbedVideoMixin
- Vimeo thumbnail





