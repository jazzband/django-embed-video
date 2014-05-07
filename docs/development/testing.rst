Testing
=======

Requirements
------------

The library needs ``Django`` and ``requests`` and ``nose``, ``mock``,
``south`` and ``testfixtures`` libraries to run tests.

::

  pip install Django
  pip install requests
  pip install nose
  pip install mock
  pip install south
  pip install testfixtures


Running tests
-------------

Run tests with this command:

::

  nosetests


Be sure to run it before each commit and fix broken tests.


Run tests with coverage:

::

  pip install coverage
  nosetests --with-coverage --cover-package=embed_video


