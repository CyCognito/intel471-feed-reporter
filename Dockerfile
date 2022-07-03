FROM python:3.8-buster

WORKDIR /app
add requirements.txt /app/requirements.txt
ADD config /app/config
ARG PYPI
RUN pip install --extra-index-url "$PYPI" -r /app/requirements.txt
add feed_reporter.py /app

RUN  adduser --home /app app && chown app /app
USER app
