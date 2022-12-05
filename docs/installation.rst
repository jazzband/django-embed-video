Installation & Setup
====================

Installation
############

The simpliest way is to use pip to install package:

.. code-block:: bash

    pip install django-embed-video


If you want latest version, you may use Git. It is fresh, but unstable.

.. code-block:: bash

    pip install git+https://github.com/jazzband/django-embed-video


Setup
#####

Add ``embed_video`` to :py:data:`~django.settings.INSTALLED_APPS` in your Django
settings.

.. code-block:: python

  INSTALLED_APPS = (
      ...
    
      'embed_video',
  )

To detect HTTP/S you must use :py:class:`~django.template.context_processors.request`
context processor:

.. code-block:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.template.context_processors.request',
    )


WSGI + Nginx
############

1. Add ``SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`` to your settings.py 
2. Add ``proxy_set_header X-Forwarded-Proto $scheme;`` to your Nginx site config file. 

This will set ``request.is_secure()`` equal to true when it is checked by ``embed_video_tags.py``, for more information reffer `here <https://github.com/jazzband/django-embed-video/issues/172#issuecomment-1335895642>`_.
