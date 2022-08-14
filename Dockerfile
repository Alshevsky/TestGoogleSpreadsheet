FROM python:3.8-slim

# set work directory
WORKDIR /code/backend/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY Pipfile /code/
RUN pip3 install --no-cache-dir pipenv==2022.1.8            \
&&  pipenv install                                          \
&&  pipenv install --system --deploy --ignore-pipfile

# copy entrypoint.sh
COPY ./run.sh /code/run.sh

# copy project
COPY . /code/

# run entrypoint.sh
ENTRYPOINT ["sh", "/code/backend/run.sh"]
