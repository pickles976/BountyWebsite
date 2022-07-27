#!/bin/bash

cd django_project
python3 manage.py makemigrations users bounty
python3 manage.py makemigrations 
python3 manage.py migrate
python3 manage.py loaddata ./bounty/fixtures/teams.json
python3 manage.py loaddata ./bounty/fixtures/wars.json