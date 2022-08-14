#!/usr/bin/env sh

pipenv shell
python3 ./manage.py migrate
python3 ./manage.py runserver 127.0.0.1:8000
daphne -b 0.0.0.0 -p 8000 app.asgi:application
