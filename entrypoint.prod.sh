#!/bin/sh

python manage.py migrate
python manage.py collectstatic --no-input
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
