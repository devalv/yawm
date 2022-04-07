FROM python:3.10-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/app
ENV APP_HOME /home/app

RUN addgroup --system app && adduser --system --group app

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
RUN chown -R app:app $APP_HOME

# install python dependencies
RUN pip install --upgrade pip
RUN pip install -U setuptools
RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

# change to the app user
USER app

# run gunicorn
# CMD gunicorn --bind 0.0.0.0:5000 main:app -k uvicorn.workers.UvicornWorker
CMD alembic upgrade head && python main.py
