# Deployment commands for silly billys

    git push heroku main

Generate random key for Django:

    import secrets
    secrets.token_hex(24)

    heroku config:set ENVIRONMENT_VAR="some variable"

Running manage.py commands in Heroku:

    heroku run python django_project/manage.py migrate

Open shell:

    heroku run bash