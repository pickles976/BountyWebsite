web: cd django_project && python manage.py migrate && gunicorn django_project.wsgi -w 3 --max-requests 50 --timeout 10

celery: python3 -m celery -A bounty beat -l info --max-interval 7200 --detach && python3 -m celery -A bounty worker -l info --detach