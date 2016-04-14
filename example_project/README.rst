Running example project
***********************

#. Install Django and PyYAML::

     pip install Django
     pip install pyyaml

#. Create database::

     python manage.py migrate --noinput

#. Run testing server::

     python manage.py runserver

#. Take a look at http://localhost:8000 . You can log in to administration with username ``admin``
   and password ``admin``.


Testing HTTPS
*************

To test HTTPS on development server, `follow these instructions
<http://www.ianlewis.org/en/testing-https-djangos-development-server>`_.
