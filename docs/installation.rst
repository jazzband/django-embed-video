Installation & Setup
====================

Installation
############

The simpliest way is to use pip to install package:

.. code-block:: bash

    pip install django-embed-video


If you want latest version, you may use Git. It is fresh, but unstable.

.. code-block:: bash

    pip install git+https://github.com/yetty/django-embed-video.git


Setup
#####

Add ``embed_video`` to :py:data:`~django.settings.INSTALLED_APPS` in your Django
settings.

.. code-block:: python

  INSTALLED_APPS = (
      ...
    
      'embed_video',
  )

To detect HTTP/S you must use :py:class:`~django.core.context_processors.request`
context processor:

.. code-block:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
    )
