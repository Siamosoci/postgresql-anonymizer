FROM python:3.8.1-slim

LABEL maintainer="webteam@rheinwerk-verlag.de"

RUN apt-get update -y \
#  && apt-get upgrade -y \ 
 && apt-get install -y libpq-dev python3-pip \
 && pip install -U pip \
#  && pip install pganonymize psycopg2-binary \
 && pip install psycopg2-binary \
 && apt-get install -y postgresql-client-common postgresql-client-11 \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY . .

RUN python3 setup.py install

