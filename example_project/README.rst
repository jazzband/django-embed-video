How to run it?
**************

#. Install Django and PyYAML::

     pip install Django
     pip install pyyaml

#. Create database::

     python manage.py syncdb --noinput

#. Run testing server::

     python manage.py runserver

#. Take a look at http://localhost:8000 . You can log in to administration with username ``admin``
   and password ``admin``.
