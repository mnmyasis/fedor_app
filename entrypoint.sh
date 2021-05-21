#!/bin/bash

cd fedor
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')"
python manage.py loaddata deploy_data.json
python manage.py loaddata group_change.json

exec gunicorn fedor.wsgi:application -b 0.0.0.0:8000 --reload