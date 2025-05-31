FROM python:3.12-slim

ENV POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

WORKDIR /app

RUN mkdir src/

COPY src/ /app/src/
COPY pyproject.toml /app
COPY poetry.lock /app
COPY Makefile /app
COPY README.md /app

RUN apt-get update && apt-get install make postgresql-client-17 -y && pip3 install --no-cache-dir poetry && poetry install --only=main --no-cache --no-interaction --no-ansi
