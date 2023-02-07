#!/bin/bash

# Collect static files
echo "Collect static files"
python3 manage.py collectstatic --no-input

echo "Wait until DB container is ready"
dockerize -wait tcp ://db:3306 -timeout 20s

echo "Migrate db"
python3 manage.py makemigrations
python3 manage.py migrate --no-input

# Start server
echo "Starting server"
# python3 manage.py runserver 0.0.0.0:8000
# gunicorn config.wsgi:application --bind 0.0.0.0:8000

exec "$@"