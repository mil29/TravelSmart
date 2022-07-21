#!/bin/bash
source /var/app/venv/staging-LQM1lest/bin/activate
python /var/app/current/manage.py migrate --noinput
