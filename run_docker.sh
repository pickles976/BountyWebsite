#!/bin/bash

cd django_project

echo $(python3 -m celery -A bounty beat -l info --logfile=celery.beat.log --max-interval 7200  --detach)
echo $(python3 -m celery -A bounty worker -l info --logfile=celery.log --detach)

python3 manage.py makemigrations users bounty
python3 manage.py makemigrations 
python3 manage.py migrate
python3 manage.py loaddata ./bounty/fixtures/teams.json
python3 manage.py loaddata ./bounty/fixtures/wars.json
python3 manage.py runserver 0.0.0.0:8000