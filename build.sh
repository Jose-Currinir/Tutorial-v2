#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install -r requirements.txt

python manage.py collectstatic --verbosity=3 --noinput
python manage.py makemigrations webpage
python manage.py migrate

echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'jpcurrinir@gmail.com', 'admin')" | python manage.py shell