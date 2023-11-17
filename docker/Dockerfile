FROM python:3.9-alpine


WORKDIR /server

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN apk update \
    && apk add postgresql-libs postgresql-dev jpeg-dev zlib-dev libjpeg gcc python3-dev musl-dev libffi-dev openssl-dev cargo

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./ ./

RUN chmod +x docker/gunicorn.sh
