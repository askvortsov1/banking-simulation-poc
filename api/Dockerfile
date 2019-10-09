FROM python:3

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./entrypoint.sh /entrypoint.sh

COPY ./src /code
WORKDIR /code
