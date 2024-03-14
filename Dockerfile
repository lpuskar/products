#FROM python:3.10.11-bullseye
#ENV TZ=Etc/UTC
#
#COPY requirements.txt /tmp/requirements.txt
#RUN pip install -r /tmp/requirements.txt
#
#WORKDIR /app
#ADD . /app
#
#EXPOSE 8000
#EXPOSE 80
#
#CMD uvicorn main:app --host 0.0.0.0 --port 8000 --reload  --log-config api/log_config.json


FROM python:3.10.11-bullseye

# Set the timezone environment variable
ENV TZ=Etc/UTC

# Install cron
RUN apt-get update && apt-get install -y cron

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /app

ADD . /app

COPY product-db-cronjobs /etc/cron.d/product-db-cronjobs

RUN chmod 0644 /etc/cron.d/product-db-cronjobs && crontab /etc/cron.d/product-db-cronjobs

RUN touch /var/log/cron.log

EXPOSE 8000
EXPOSE 80

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]