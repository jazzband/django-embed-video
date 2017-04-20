Running example project
***********************

#. Install requirements::

     pip install -r requirements.txt

#. Create database::

     python manage.py migrate --run-syncdb --noinput

   Or, for older versions of Django::

     python manage.py syncdb --noinput

#. Run testing server::

     python manage.py runserver

#. Take a look at http://localhost:8000 . You can log in to administration with username ``admin``
   and password ``admin``.


Testing HTTPS
*************

To test HTTPS on development server, `follow this instructions
<http://www.ianlewis.org/en/testing-https-djangos-development-server>`_.
