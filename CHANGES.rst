
Changes
=======

Unreleased
----------


Release 1.4.2 (March 17, 2022)
------------------------------

- Add Polish translation


Release 1.4.1 (January 6, 2022)
---------------------------------

- Add Code of Conduct to repository
- Add support for Python 3.10
- Add support for Django 3.2 and Django 4.0
- Drop support for EOL Python 3.6
- Drop support for EOL Django 3.0 and EOL Django 3.1
- Remove Nose from dependencies due to version incompatibility


Release 1.4.0 (December 18, 2020)
---------------------------------

- Add lazy loading for video template tags.
- Handle Vimeo admin "manage" URLs
- Migrate from Travis CI to GitHub Actions.
- Drop unsupported Django versions prior to 2.2.
- Add support for Python up to 3.9.
- Add support for Django up to 3.1.
- Improve code formatting.


Release 1.3.3 (June 10, 2020)
-----------------------------

- Fix admin UI exception with form validation.


Release 1.3.2 (March 29, 2020)
------------------------------

- Add support for Soundcloud mobile URLs.


Release 1.3.1 (January 6, 2020)
-------------------------------

- Add support for Vimeo review video URLs.
- Update example project code.


Release 1.3 (August 30, 2019)
-----------------------------

- Drop unsupported Python version prior to 3.6.
- Drop unsupported Django versions prior to 1.11.
- Add support for Python up to 3.8 including PyPy.
- Add support for Django up to 2.2.
- Improve project structure, docs and language.
- Improve CI and CD infrastructure and automation.
- Move project to Jazzband organization.


Release 1.2.0 (October 04, 2018)
--------------------------------

- hotfix docs directive
  (`#94 <https://github.com/jazzband/django-embed-video/pull/94>`_)

- update docs
  (`#92 <https://github.com/jazzband/django-embed-video/pull/92>`_)

- use tests_require and setup_requires for nose testing requirements
  (`#91 <https://github.com/jazzband/django-embed-video/pull/91>`_)

- add renderer kwarg to Widget render method to support Python 2.1 and later
  (`#88 <https://github.com/jazzband/django-embed-video/pull/88>`_)

- enable default HTTPS support for YouTube, VimeoBackend, SoundCloudBackend
  (`#86 <https://github.com/jazzband/django-embed-video/pull/86>`_)

- added syntax highlight in README.rst
  (`#81 <https://github.com/jazzband/django-embed-video/pull/81>`_)

- updating requests >=2.19


Release 1.1.2 (April 27, 2017)
------------------------------

- fix pypi


Release 1.1.1 (March 24, 2017)
------------------------------

- updates for Django 1.10 and 1.11
  (`#73 <https://github.com/jazzband/django-embed-video/pull/73>`_)

- update requirements for installation of the example project
  (`#72 <https://github.com/jazzband/django-embed-video/pull/72>`_)

- use secure connection to query soundcloud endpoint
  (`#68 <https://github.com/jazzband/django-embed-video/pull/68>`_)



Release 1.1.0 (Jan 19, 2016)
----------------------------

- added support fort Django 1.9
  (`#52 <https://github.com/jazzband/django-embed-video/issues/52>`_)

- if possible YouTube thumbnails are returned in better resolution
  (`#43 <https://github.com/jazzband/django-embed-video/issues/43>`_)


Release 1.0.0 (May 01, 2015)
----------------------------

**Backward incompatible changes:**

- filter `embed_video_tags.embed` has been removed

- changed behaviour of extra params in video tag
  (`#34 <https://github.com/jazzband/django-embed-video/issues/34>`_, `#36 <https://github.com/jazzband/django-embed-video/pull/36>`_)


Backward compatible changes:

- added support for Django 1.7 and Django 1.8

- added support for Vimeo channels
  (`#47 <https://github.com/jazzband/django-embed-video/pull/47>`_)

- fix resizing of SoundCloud iframe
  (`#41 <https://github.com/jazzband/django-embed-video/pull/41>`_)


Release 0.11 (July 26, 2014)
----------------------------

- add support for YouTube mobile urls
  (`#27 <https://github.com/jazzband/django-embed-video/pull/27>`_)

- fix passing parameters in calling request library
  (`#28 <https://github.com/jazzband/django-embed-video/pull/28>`_)

- fix validation of urls
  (`#31 <https://github.com/jazzband/django-embed-video/issues/31>`_)


Release 0.10 (May 24, 2014)
---------------------------

- ``video`` tag accepts kwargs
  (`#20 <https://github.com/jazzband/django-embed-video/pull/20>`_)

- ``video`` tag will not crash anymore with ``None`` passed as url
  (`#24 <https://github.com/jazzband/django-embed-video/issues/24>`_)


Release 0.9 (Apr. 04, 2014)
---------------------------

- Add ``VideoBackend.template_name`` and rendering embed code from file.

- Allow relative sizes in template tag
  (`#19 <https://github.com/jazzband/django-embed-video/pull/19>`_).

- Fix handling invalid urls of SoundCloud.
  (`#21 <https://github.com/jazzband/django-embed-video/issues/21>`_).

- Catch ``VideoDoesntExistException`` and ``UnknownBackendException`` in
  template tags and admin widget.

- Add base exception ``EmbedVideoException``.


Release 0.8 (Feb. 22, 2014)
---------------------------

- Add ``EMBED_VIDEO_TIMEOUT`` to settings.

- Fix renderering template tag if no url is provided
  (`#18 <https://github.com/jazzband/django-embed-video/issues/18>`_)

- If ``EMBED_VIDEO_TIMEOUT`` timeout is reached in templates, no exception is
  raised, error is just logged.

- Fix default size in template tag.
  (`See more... <https://github.com/jazzband/django-embed-video/commit/6cd3567197d6fdc31bc63fb799815e8368128b90>`_)


Release 0.7 (Dec. 21, 2013)
---------------------------

- Support for sites running on HTTPS

- ``embed`` filter is deprecated and replaced by ``video`` filter.

- caching for whole backends was removed and replaced by caching properties

- minor improvements on example project (fixtures, urls)


Release 0.6 (Oct. 04, 2013)
---------------------------

- Ability to overwrite embed code of backend

- Caching backends properties

- PyPy compatibility

- Admin video mixin and video widget


Release 0.5 (Sep. 03, 2013)
---------------------------

- Added Vimeo thumbnails support

- Added caching of results

- Added example project

- Fixed template tag embed

- Fixed raising UnknownIdException in YouTube detecting.



Release 0.4 (Aug. 22, 2013)
---------------------------

- Documentation was rewrited and moved to http://django-embed-video.rtfd.org/ .

- Custom backends
  (http://django-embed-video.rtfd.org/en/latest/examples.html#custom-backends).

- Improved YouTube and Vimeo regex.

- Support for Python 3.

- Renamed ``base`` to ``backends``.



Release 0.3 (Aug. 20, 2013)
---------------------------

- Security fix: faked urls are treated as invalid. See `this page
  <https://github.com/jazzband/django-embed-video/commit/d0d357b767e324a7cc21b5035357fdfbc7c8ce8e>`_
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
---------------------------

- Support of SoundCloud

Release 0.1 (June 1, 2013)
--------------------------

- Initial release
