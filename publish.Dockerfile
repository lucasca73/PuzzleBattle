FROM ruby:2.3.8-alpine

WORKDIR /code

RUN gem install u3d

RUN export LC_ALL=en_US.UTF-8
RUN export LANG=en_US.UTF-8