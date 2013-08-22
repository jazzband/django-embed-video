Installation & Setup
==============================================

Installation
##############################################

Use pip to install package:

::

    pip install django-embed-video


If you want latest version, you may use Git. It is fresh, but unstable.

::

    pip install git+https://github.com/yetty/django-embed-video.git


Setup
##############################################

Add ``embed_video`` to :py:data:`~django.settings.INSTALLED_APPS` in your Django
settings.

::

  INSTALLED_APPS = (
      ...
    
      'embed_video',
  )

