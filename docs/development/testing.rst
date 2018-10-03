Testing
=======

Requirements
------------

The library needs ``Django`` and ``requests`` and ``nose``, ``mock``,
``south`` and ``testfixtures`` libraries to run tests.  They will be installed
automatically when running tests via setup.py

::


Running tests
-------------

Run tests with this command:

::

  python setup.py nosetests


Be sure to run it before each commit and fix broken tests.


Run tests with coverage:

::

  python setup.py nosetests --with-coverage --cover-package=embed_video


