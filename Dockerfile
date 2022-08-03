# pull official base image
FROM python:3.8-slim-buster

# set work directory
WORKDIR /code/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY Pipfile /code/
RUN pip3 install pipenv
RUN pipenv install
RUN pipenv install --system --deploy --ignore-pipfile
RUN pip install celery



# copy project
COPY . /code/