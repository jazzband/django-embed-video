Testing
=======

Requirements
------------

The library needs a copy of ``Django``, e.g.::

  pip install Django

And several libraries that can be installed from the root of
a source checkout::

  pip install  -r embed_video/tests/test-requirements.txt

It's recommended to make a separate virtual environment where you
install these packages.

Running tests
-------------

Run tests in your virtual environment with this command:

::

  nosetests


Be sure to run it before each commit and fix broken tests.


Run tests with coverage:

::

  nosetests --with-coverage --cover-package=embed_video

Use tox if you want to test against all supported Django versions,
similar to the Travis build. Install it once::

  pip install tox>=2.0

Run the tests with::

  tox
