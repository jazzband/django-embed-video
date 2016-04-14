Installation & Setup
====================

Installation
############

The simpliest way is to use pip to install the package:

.. code-block:: bash

    pip install django-embed-video


If you want the latest version, you may use Git. It is fresh, but unstable.

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

To detect HTTP/S you must add the :py:class:`~django.template.context_processors.request`
(or :py:class:`~django.core.context_processors.request` for Django < 1.9) context
processor:

.. code-block:: python

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'django.core.context_processors.request',
    )
