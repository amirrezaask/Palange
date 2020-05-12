FROM python:3.6

RUN apt-get update -qq && apt-get install -qqy netcat

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . /palange
WORKDIR /palange/src/

ENTRYPOINT ["bash", "./../docker-entrypoint.sh"]