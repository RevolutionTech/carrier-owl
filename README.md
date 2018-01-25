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

### Installation

Then in your virtual environment, you will need to install Python dependencies such as [Django](https://www.djangoproject.com/), psycopg2, and django-classbasedsettings. You can do this simply with the command:

    pip install -r requirements.txt

### Configuration

Next we will need to set up some environment variables for your dev instance of Carrier Owl. These values should be kept secret. Add a secret key and the database credentials to your `~/.bashrc` file:

    export CARRIER_OWL_SECRET_KEY='-3f5yh&(s5%9uigtx^yn=t_woj0@90__fr!t2b*96f5xoyzb%b'
    export CARRIER_OWL_DATABASE_URL='postgres://postgres:abc123@localhost:5432/carrier_owl'
    export CARRIER_OWL_GOOGLE_OAUTH2_CLIENT_ID='1234-abc123.apps.googleusercontent.com'
    export CARRIER_OWL_GOOGLE_OAUTH2_CLIENT_SECRET='abc123'

For reference, the format of the `DATABASE_URL` is as follows:

    postgres://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}

Of course you should [generate your own secret key](http://stackoverflow.com/a/16630719) and use a more secure password for your database. Also, be sure that special characters (such as `?` and `#`) in your `DATABASE_URL` are percent-encoded. Then source your `~/.bashrc` file to set these environment variables:

    source ~/.bashrc

With everything installed and all files in place, you may now create the database tables. You can do this with:

    python manage.py migrate
