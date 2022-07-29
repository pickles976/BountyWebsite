web: cd django_project && python manage.py migrate && gunicorn django_project.wsgi

celery_beat: python3 -m celery -A bounty beat -l info --max-interval 7200 --detach
celery_worker: python3 -m celery -A bounty worker -l info --logfile=celery.log --detach