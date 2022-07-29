# Deployment commands for silly billys

## Subsequent changes:

Push Changes:

    git push heroku main

Run Celery:

    heroku run bash

    cd django_project

    python3 -m celery -A bounty beat -l info --logfile=celery.beat.log --max-interval 7200  --detach 
    python3 -m celery -A bounty worker -l info --logfile=celery.log --detach


## First-Time setup:

Generate random key for Django:

    import secrets
    secrets.token_hex(24)

    heroku config:set ENVIRONMENT_VAR="some variable"

Running manage.py commands in Heroku:

    heroku run python django_project/manage.py migrate

Connecting to Redis in Heroku:

    heroku redis:credentials REDIS_URL

Refreshing Redis Credentials:

    heroku redis:credentials HEROKU_REDIS_GRAY_URL --reset