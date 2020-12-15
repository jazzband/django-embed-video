django-embed-video
==================

Django app for easy embedding YouTube and Vimeo videos and music from SoundCloud.

.. image:: https://jazzband.co/static/img/badge.svg
   :target: https://jazzband.co/
   :alt: Jazzband
.. image:: https://github.com/jazzband/django-embed-video/workflows/Test/badge.svg
   :target: https://github.com/jazzband/django-embed-video/actions
   :alt: GitHub Actions
.. image:: https://coveralls.io/repos/yetty/django-embed-video/badge.svg?branch=master
   :target: https://coveralls.io/r/yetty/django-embed-video?branch=master
   :alt: Coveralls coverage percentage
.. image:: https://img.shields.io/pypi/pyversions/django-embed-video.svg
   :target: https://pypi.org/project/django-embed-video/
   :alt: Supported Python versions
.. image:: https://img.shields.io/pypi/djversions/django-embed-video.svg
   :target: https://pypi.org/project/django-embed-video/
   :alt: Supported Django versions


Documentation
-------------

Documentation is at: http://django-embed-video.rtfd.org/


Quick start
-----------

#. Install ``django-embed-video``:

   ::

      pip install django-embed-video


   or from sources

   ::

      pip install git+https://github.com/jazzband/django-embed-video


#. Add ``embed_video`` to ``INSTALLED_APPS`` in your Django settings.

#. If you want to detect HTTP/S in template tags, you have to set ``request``
   context processor in ``settings.TEMPLATES``:

   .. code-block:: python

       TEMPLATES = [
           {
               'BACKEND': 'django.template.backends.django.DjangoTemplates',
               # ...
               'OPTIONS': {
                   'context_processors': [
                       # ...
                       'django.template.context_processors.request',
                   ],
               },
           },
       ]

#. Usage of template tags:

   .. code-block:: html+django

      {% load embed_video_tags %}

      <!-- The video tag: -->
      {% video item.video as my_video %}
        URL: {{ my_video.url }}
        Thumbnail: {{ my_video.thumbnail }}
        Backend: {{ my_video.backend }}

        {% video my_video "large" %}
      {% endvideo %}

      <!-- Or embed shortcut: -->
      {% video my_video '800x600' %}

#. Usage of model fields

   .. code-block:: python

      from django.db import models
      from embed_video.fields import EmbedVideoField

      class Item(models.Model):
          video = EmbedVideoField()  # same like models.URLField()


Contributing
------------

This is a `Jazzband <https://jazzband.co>`_ project.
By contributing you agree to abide by the `Contributor Code of Conduct <https://jazzband.co/about/conduct>`_
and follow the `guidelines <https://jazzband.co/about/guidelines>`_.
