FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/app
ENV APP_HOME /home/app
ENV API_HOST 0.0.0.0
ENV API_PORT 5000

RUN mkdir -p $APP_HOME

WORKDIR $APP_HOME

RUN set -ex \
    \
    && apt-get update \
    && apt-get install -y netcat gcc libpq-dev \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# chown all the files to the app user
COPY ./backend/ .

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -U setuptools
RUN pip install poetry

RUN poetry export --dev -f requirements.txt --output dev-requirements.txt
RUN pip install -r dev-requirements.txt


# run tests
CMD python -m pytest
