web: cd django_project && python manage.py migrate && gunicorn django_project.wsgi

worker: cd django_project && python3 -m celery -A bounty beat -l info --max-interval 7200  --detach && python3 -m celery -A bounty worker -l info --detach