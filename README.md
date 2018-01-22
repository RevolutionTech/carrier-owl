# Carrier Owl
#### Assistant for sending out personalized invitations

## Setup

### Prerequisites

Carrier Owl requires [PostgreSQL](http://www.postgresql.org/) and pip, which you can install on debian with:

    sudo apt-get install postgresql postgresql-contrib libpq-dev python-pip python-dev

I recommend using a virtual environment for Carrier Owl. If you don't have it already, you can install [virtualenv](http://virtualenv.readthedocs.org/en/latest/virtualenv.html) and virtualenvwrapper globally with pip:

    sudo pip install virtualenvwrapper

[Update your .profile or .bashrc file](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file) to create new environment variables for virtualenvwrapper and then create and activate your virtual environment with:

    mkvirtualenv carrier-owl

In the future you can reactivate the virtual environment with:

    workon carrier-owl
