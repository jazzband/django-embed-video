django-embed-video
==================

Django app for easy embeding YouTube and Vimeo videos and music from SoundCloud.

.. image:: https://travis-ci.org/yetty/django-embed-video.png?branch=master
    :target: https://travis-ci.org/yetty/django-embed-video
.. image:: https://coveralls.io/repos/yetty/django-embed-video/badge.png?branch=master
    :target: https://coveralls.io/r/yetty/django-embed-video?branch=master
.. image:: https://pypip.in/v/django-embed-video/badge.png
    :target: https://crate.io/packages/django-embed-video/
.. image:: https://pypip.in/d/django-embed-video/badge.png
    :target: https://crate.io/packages/django-embed-video/


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
---------------

Using the EmbedVideoField provides you validation of URLs.

::

    from django.db import models
    from embed_video.fields import EmbedVideoField

    class Item(models.Model):
        video = EmbedVideoField()  # same like models.URLField()




Contributing
*************

I will be really pleased if you will provide patch to this Django app. Feel free
in changing source code, but please keep `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_
rules and `Zen <http://www.python.org/dev/peps/pep-0020/>`_.



TODO
*****

- provide AdminEmbedVideoMixin
- Vimeo thumbnail


.. vim: set tw=80:



