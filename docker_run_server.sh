#!/bin/sh
set -e

python manage.py migrate --noinput

exec gunicorn university_marketplace.wsgi:application \
  --bind 0.0.0.0:80 \
  --workers 3
