FROM	python:3.6 AS build

RUN		apt-get update
RUN		apt-get install uwsgi -y

RUN		pip3 install --upgrade pip
RUN		pip3 install Django
RUN		pip3 install psycopg2-binary
RUN     pip3 install requests
RUN		pip3 install uwsgi