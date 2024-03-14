#!/bin/bash

service cron start

exec uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-config log_config.json