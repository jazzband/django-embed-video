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

Documentation
*************

Documentation is here: http://django-embed-video.rtfd.org/


Quick start
************

#. Install ``django-embed-video``:

   ::

      pip install django-embed-video


   or from sources

   ::

      pip install git+https://github.com/yetty/django-embed-video.git


#. Add ``embed_video`` to ``INSTALLED_APPS`` in your Django settings.


#. Use template tags:

   ::

      {% load embed_video_tags %}

      The video tag:
      {% video item.video as my_video %}
        URL: {{ my_video.url }}
        Thumbnail: {{ my_video.thumbnail }}
        Backend: {{ my_video.backend }}
      {% endvideo %}

      Or embed shortcut:
      {{ my_video|embed:'800x600' }}

#. Use model fields

   ::

      from django.db import models
      from embed_video.fields import EmbedVideoField

      class Item(models.Model):
          video = EmbedVideoField()  # same like models.URLField()


.. vim: set tw=80:
