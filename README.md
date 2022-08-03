# TestGoogleSpreadsheet

## Install

1. Install Docker and docker-compose.
   
For Debian, Ubuntu:

```
su
apt update; apt upgrade -y; apt install -y curl; curl -sSL https://get.docker.com/ | sh; curl -L https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose
```

Don't forget press CTRL+D to exit from superuser account.

2. Apply environment variables:

```
cp example.env .env
```

3. Change a random string for `SECRET_KEY` in `.env`.
4. Add your `SPREADSHEET_ID` and `API_KEY` in `.env`.

5. Install dependencies:

```
pipenv install
pipenv shell
```

6. Up docker-compose, migrate database and create super user:

```
docker-compose up -d
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

7. Run the server:

```
python3 manage.py runserver
```

## celery start 
```
celery -A app worker -l info -B
```

7. Enjoy!

https://docs.google.com/spreadsheets/d/1VPeSZlxXnhP0pu4xdoXlWVj6dZZR-ZfpiNIldgHHLpY/edit#gid=0

api = AIzaSyDCT2lgkKdmbMJlcUKNQPi1w66UGy75_9g
