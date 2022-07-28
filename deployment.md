# Deployment commands for silly billys

    git push heroku main

Generate random key:

    import secrets
    secrets.token_hex(24)

    heroku config:set ENVIRONMENT_VAR="some variable"