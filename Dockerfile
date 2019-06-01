FROM python:3.7-alpine

MAINTAINER mintplo "iam@mintplo.me"

ENV PYTHON_VERSION=3.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_DOWNLOAD_CACHE /cache/pip

RUN mkdir -p /baro/src

COPY Pipfile Pipfile.lock /baro/src/
WORKDIR /baro/src
RUN apk add --no-cache mariadb-connector-c-dev ;\
    apk add --no-cache --virtual .build-deps \
        build-base \
        mariadb-dev ;\
    pip install pipenv && pipenv install --system --ignore-pipfile --dev;\
    apk del .build-deps

COPY . /baro/src

EXPOSE 8000

CMD ["gunicorn", "-c", "config/gunicorn.py", "--bind", ":8000", "run:app"]
