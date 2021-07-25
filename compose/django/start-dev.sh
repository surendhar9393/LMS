#!/bin/sh
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

#celery -A LMS worker -l info
