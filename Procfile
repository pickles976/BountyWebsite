web: cd django_project && python manage.py migrate && gunicorn django_project.wsgi -w 3 --max-requests 50 --timeout 60

celery: cd django_project && python3 -m celery -A bounty beat -l info --logfile=celery.beat.log --max-interval 7200 --detach && python3 -m celery -A bounty worker -l info --logfile=celery.log