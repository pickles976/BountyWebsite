web: cd django_project && python manage.py migrate && gunicorn -k gevent django_project.wsgi --max-requests 1000

celery: python3 -m celery -A bounty beat -l info --max-interval 7200 --detach && python3 -m celery -A bounty worker -l info --detach