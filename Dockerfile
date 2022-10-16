# syntax=docker/dockerfile:1
FROM python:3
RUN pip install --upgrade pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
# install ffmpeg
RUN apt-get update && apt-get install ffmpeg -y
# setup cron
RUN apt-get update && apt-get install -y cron
COPY manage_audio /etc/cron.d/manage_audio
RUN chmod 0644 /etc/cron.d/manage_audio && crontab /etc/cron.d/manage_audio
# init dialo model
RUN python core/chat/convo_ai.py -s
