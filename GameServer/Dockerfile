# FROM python:3.5.6-slim-stretch
FROM python:2.7-slim-jessie

ADD . /code
WORKDIR /code

RUN apt-get update && apt-get install git -y

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
