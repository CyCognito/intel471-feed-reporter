FROM python:3.8-buster
add requirements.txt /
ADD config /config
ARG PYPI
RUN pip install --extra-index-url "$PYPI" -r requirements.txt
add feed_reporter.py /
