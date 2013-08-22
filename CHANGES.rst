Release 0.3 (Aug. 20, 2013)
----------------------------

- Security fix: faked urls are treated as invalid. See `this page
  <https://github.com/yetty/django-embed-video/commit/d0d357b767e324a7cc21b5035357fdfbc7c8ce8e>`_
  for more details. 

- Fixes:
  
  - allow of empty video field.

  - requirements in setup.py

- Added simplier way to embed video in one-line template tag::

    {{ 'http://www.youtube.com/watch?v=guXyvo2FfLs'|embed:'large' }}

- ``backend`` variable in ``video`` template tag.

  Usage::
      
    {% video item.video as my_video %}
        Backend: {{ my_video.backend }}
    {% endvideo %}


Release 0.2 (June 25, 2013) 
----------------------------

- Support of SoundCloud

Release 0.1 (June 1, 2013)
----------------------------

- Initial release
