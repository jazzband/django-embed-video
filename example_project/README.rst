Running example project
***********************

#. Install Django and PyYAML::

     pip install Django
     pip install pyyaml

#. Create database::

     python manage.py migrate --noinput

#. And superuser::

     python manage.py createsuperuser

#. Run testing server::

     python manage.py runserver

#. Create new posts at http://localhost:8000/admin/ and view them on http://localhost:8000.


Testing HTTPS
*************

To test HTTPS on a development server, `follow these instructions
<http://www.ianlewis.org/en/testing-https-djangos-development-server>`_.
