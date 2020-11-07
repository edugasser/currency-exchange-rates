#!/bin/sh

# # Collect static files
#echo "Collect static files"
#python app/manage.py collectstatic --noinput
#
## Apply database migrations
#echo "Apply database migrations"
#python app/manage.py migrate
#
## Start server
#echo "Starting server"
#
#python app/manage.py runserver 0.0.0.0:8000
while true
do
    echo "Press [CTRL+C] to stop.."
    sleep 1
done
