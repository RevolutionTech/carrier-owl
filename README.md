# Carrier Owl
#### Assistant for sending out personalized invitations

[![Build Status](https://travis-ci.com/RevolutionTech/carrier-owl.svg?branch=master)](https://travis-ci.com/RevolutionTech/carrier-owl)
[![codecov](https://codecov.io/gh/RevolutionTech/carrier-owl/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/carrier-owl)

## Setup

### Prerequisites

Carrier Owl requires [SQLite](https://www.sqlite.org/index.html) and Python header files, which you can install on debian with:

    sudo apt-get install libsqlite3-dev python3-dev

### Installation

Use [poetry](https://github.com/sdispater/poetry) to install Python dependencies:

    poetry install

### Configuration

Next we will need to set up some environment variables for your dev instance of Carrier Owl, such as your secret key and database credentials. Be sure to keep secret values secret! Add these values to your `~/.bashrc` file:

    export CARRIER_OWL_SECRET_KEY='-3f5yh&(s5%9uigtx^yn=t_woj0@90__fr!t2b*96f5xoyzb%b'
    export CARRIER_OWL_GOOGLE_OAUTH2_CLIENT_ID='1234-abc123.apps.googleusercontent.com'
    export CARRIER_OWL_GOOGLE_OAUTH2_CLIENT_SECRET='abc123'

    # Event details
    export CARRIER_OWL_EVENT_WEEKDAY=2  # Wednesday
    export CARRIER_OWL_EVENT_START_HOUR=14  # 2pm
    export CARRIER_OWL_EVENT_START_MINUTE=0
    export CARRIER_OWL_EVENT_END_HOUR=15  # 3pm
    export CARRIER_OWL_EVENT_END_MINUTE=0
    export CARRIER_OWL_EVENT_SUMMARY='Example title'
    export CARRIER_OWL_EVENT_DESCRIPTION='Example description'  # optional
    export CARRIER_OWL_EVENT_LOCATION='San Francisco, CA'  # optional
    export CARRIER_OWL_EVENT_ATTENDEES='jsmith@example.com,mdoe@example.com'  # optional

Of course you should [generate your own secret key](http://stackoverflow.com/a/16630719) and use a more secure password for your database. Then source your `~/.bashrc` file to set these environment variables:

    source ~/.bashrc

With everything installed and all files in place, you may now create the database tables. You can do this with:

    poetry run python manage.py migrate

### Deployment

Deployments are done using `zappa`. First, you will need to decrypt the `zappa_settings.json.enc` to `zappa_settings.json`:

    openssl aes-256-cbc -k $DECRYPT_PASSWORD -in zappa_settings.json.enc -out zappa_settings.json -d

where `$DECRYPT_PASSWORD` contains the key that the settings were encrypted with. Then, use `zappa` to deploy to the production environment:

    poetry run zappa deploy

Once deployed, you will need to set environment variables on the generated Lambda. In addition to the environment variables for the development environment, you will also need to provide two additional environment variables: `CARRIER_OWL_AWS_ACCESS_KEY_ID` and `CARRIER_OWL_AWS_SECRET_ACCESS_KEY`.

Then to publish static assets, run the `manage.py collectstatic` command locally, using the production environment variables listed above:

    STAGE=production CARRIER_OWL_AWS_ACCESS_KEY_ID=1234 CARRIER_OWL_AWS_SECRET_ACCESS_KEY=abc123 poetry run python manage.py collectstatic --noinput

You may also need to update `ALLOWED_HOSTS` in `settings/prod.py` to match the assigned URL for the Lambda. Once completed, the assigned URL should be running Carrier Owl.

If any changes to `zappa_settings.json` are made, the file should be re-encrypted before being committed. The following bash functions may be helpful for encrypting/decrypting:

    function encrypt_openssl () { openssl aes-256-cbc -k $DECRYPT_PASSWORD -in "$1" -out "$1".enc; }
    function decrypt_openssl () { openssl aes-256-cbc -k $DECRYPT_PASSWORD -in "$1".enc -out "$1" -d; }
