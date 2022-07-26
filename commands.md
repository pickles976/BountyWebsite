# Commands for running Django

    python manage.py makemigrations users
    python manage.py makemigrations bounty
    python manage.py migrate
    python manage.py loaddata .\bounty\fixtures\teams.json
    python manage.py loaddata .\bounty\fixtures\wars.json
    python manage.py createsuperuser
    python manage.py runserver

# run redis broker in docker
    docker run -p 6379:6379 --name some-redis -d redis

# celery test
    python3 -m celery -A bounty worker -l info
    celery -A simpletask beat -l info

# run celery task workers and beat
    pkill -f "celery worker"  
    python3 -m celery -A bounty beat -l info --logfile=celery.beat.log --max-interval 7200  --detach 
    python3 -m celery -A bounty worker -l info --logfile=celery.log

# terminate all processes

    kill -9 $(ps aux | grep celery | grep -v grep | awk '{print $2}' | tr '\n'  ' ') > /dev/null 2>&1