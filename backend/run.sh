#!/usr/bin/env sh

python3 ./manage.py migrate
daphne -b 0.0.0.0 -p 8080 app.asgi:application