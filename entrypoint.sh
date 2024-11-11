#!/bin/sh
python manage.py migrate
uwsgi --http 0.0.0.0:8000 --chdir /app --module django_server.wsgi:application
