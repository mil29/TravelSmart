#!/bin/bash
cd /var/app/current/
source /var/app/venv/*/bin/activate
python manage.py migrate --noinput
