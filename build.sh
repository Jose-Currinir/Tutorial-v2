#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py makemigrations webpage
python manage.py migrate

from django.contrib.auth.models import User
superuser = User.objects.create_superuser('admin', 'jpcurrinir@gmail.com', 'admin')
superuser.save()