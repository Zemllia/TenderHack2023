#!/bin/sh

# collect static files
python manage.py collectstatic --noinput
# make sure to migrate
python manage.py migrate --noinput

# run gunicorn
gunicorn -b 0.0.0.0:5000 TenderHack.wsgi --workers 15 $* --reload --timeout=120
#gunicorn -b unix:/gunicorn_socket/socket TenderHack.wsgi --workers 3 $*
