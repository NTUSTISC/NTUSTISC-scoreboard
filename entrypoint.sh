#!/bin/bash
/usr/local/bin/python3 manage.py makemigrations
/usr/local/bin/python3 manage.py makemigrations index
/usr/local/bin/python3 manage.py migrate
# /usr/local/bin/python3 manage.py shell < postgresql.py
/usr/local/bin/uwsgi --ini uwsgi.ini
# /usr/local/bin/python3 manage.py runserver 0.0.0.0:8000