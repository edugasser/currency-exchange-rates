#!/bin/sh

# # Collect static files
echo "Collect static files"
python src/manage.py collectstatic --noinput

## Apply database migrations
echo "Apply database migrations"
python src/manage.py makemigrations
python src/manage.py migrate

echo "Initial setup"
python src/manage.py loaddata initial_setup.json
python src/manage.py loaddata initial_setup_user.json


## Start server
echo "Starting server"
python src/manage.py runserver 0.0.0.0:8000
