# How to run in Docker:

    docker-compose up

Open the docker Terminal  

    cd django_project

Run Celery beat and workers with:  

    python3 -m celery -A bounty beat -l info --logfile=celery.beat.log --max-interval 7200  --detach 
    python3 -m celery -A bounty worker -l info --logfile=celery.log --detach

Run the server:  

    python3 manage.py runserver 0.0.0.0:8000

If working, the beat logs should show successful dispatches and the worker logs should show successful execution. Any messages in the db should be sent over Discord once a minute, and a new War should be started and all players de-verified after 10 mins.

# Other Commands:

## Loading fixtures

    python manage.py loaddata .\bounty\fixtures\teams.json
    python manage.py loaddata .\bounty\fixtures\wars.json

## CELERY BULLSHIT (WINDOWS)

### Run redis broker in docker
    docker run -p 6379:6379 --name some-redis -d redis

### Celery test
    python3 -m celery -A bounty beat -l info
    python3 -m celery -A bounty worker -l info

### Run celery task workers and beat with logs
    python3 -m celery -A bounty beat -l info --logfile=celery.beat.log --max-interval 7200
    python3 -m celery -A bounty worker -l info --logfile=celery.log

The Celery worker will fail because Shindows. You will need to run inside of a Docker container to fully test the workers.

