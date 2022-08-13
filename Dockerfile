FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

COPY Pipfile Pipfile.lock /code/

WORKDIR /code

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

COPY backend /code/backend/

COPY run.sh /code/
COPY uwsgi.ini /code/
#ENTRYPOINT ["sh", "/run.sh"]
#ENTRYPOINT ["/backend/run.sh"]
#CMD ["chmod +x", "/run.sh"]

RUN mkdir -p /var/log/uwsgi/
WORKDIR /code/backend/

EXPOSE 8080
