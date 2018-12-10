# FROM python:3.5.6-slim-stretch
FROM python:2.7.15-alpine

ADD . /code
WORKDIR /code/GameServer

RUN pip install --upgrade pip
RUN pip install -r requirements/dev.txt

RUN apt-get install git -y