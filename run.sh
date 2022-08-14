#!/usr/bin/env sh

pipenv shell
python3 ./manage.py migrate
python3 ./manage.py runserver
daphne -b 0.0.0.0 -p 8080 app.asgi:application
