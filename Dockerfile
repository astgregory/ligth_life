FROM python:3.10-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY ligthlife /ligthlife
WORKDIR /ligthlife
EXPOSE 8000

RUN apk update

RUN apk add postgresql-client build-base postgresql-dev gcc python3-dev musl-dev libpq-dev

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password ligthlife-user

USER ligthlife-user