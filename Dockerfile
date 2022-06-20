FROM python:3.8-buster
add requirements.txt /
RUN pip install -r requirements.txt
add feed_reporter.py /
