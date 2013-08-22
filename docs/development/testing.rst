Testing
==============================================

Requirements
-------------

You need ``nose``, ``mock`` and ``south`` libraries to run tests.

:: 

  pip install nose
  pip install mock
  pip install south


Running tests
------------------

Run tests with this command:

::

  python setup.py test


Be sure to run it before each commit and fix broken tests.


Run tests with coverage:

::
  
  coverage run setup.py test 
  coverage report
