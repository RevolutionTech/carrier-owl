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
