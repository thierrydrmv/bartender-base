#!/usr/bin/env bash

set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py tailwind install
python manage.py tailwind build
python manage.py collectstatic --noinput