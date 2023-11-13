FROM python:3.10

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

ADD . /app