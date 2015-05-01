django-embed-video
==================

Django app for easy embedding YouTube and Vimeo videos and music from SoundCloud.

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

#. If you want to detect HTTP/S in template tags, you have to set ``request``
   context processor in ``settings.TEMPLATE_CONTEXT_PROCESSORS``:

   ::

       TEMPLATE_CONTEXT_PROCESSORS = (
           ...
           'django.core.context_processors.request',
       )

#. Usage of template tags:

   ::

      {% load embed_video_tags %}

      The video tag:
      {% video item.video as my_video %}
        URL: {{ my_video.url }}
        Thumbnail: {{ my_video.thumbnail }}
        Backend: {{ my_video.backend }}

        {% video my_video "large" %}
      {% endvideo %}

      Or embed shortcut:
      {% video my_video '800x600' %}

#. Usage of model fields

   ::

      from django.db import models
      from embed_video.fields import EmbedVideoField

      class Item(models.Model):
          video = EmbedVideoField()  # same like models.URLField()

