# Carrier Owl
#### Assistant for sending out personalized invitations

![CI](https://github.com/RevolutionTech/carrier-owl/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/RevolutionTech/carrier-owl/branch/master/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/carrier-owl)

## Setup

### Installation

Use [poetry](https://github.com/sdispater/poetry) to install Python dependencies:

    poetry install

### Configuration

Carrier Owl reads in environment variables from your local `.env` file. See `.env-sample` for configuration options. Be sure to [generate your own secret key](http://stackoverflow.com/a/16630719).

With everything installed and all files in place, you may now create the database tables. You can do this with:

    poetry run python manage.py migrate

### Deployment

Carrier Owl is deployed as a `zappa` app on AWS Lambda. To modify the deployment settings, first you will need to decrypt `zappa_settings.json`:

    DECRYPT_PASSWORD=abc123 poetry run inv openssl.decrypt zappa_settings.json

where `DECRYPT_PASSWORD` is assigned to the key that the settings were encrypted with.

Then, generate a Docker container and run the container to execute zappa commands, such as `zappa update`:

    poetry run inv deploy

The `inv deploy` command also updates static files via `./manage.py collectstatic`.

Once deployed, you will need to set environment variables on the generated Lambda. See `ProdConfig` for additional environment variables used in production. You may also need to update `ALLOWED_HOSTS` in `ProdConfig` to match the assigned URL for the Lambda. Once completed, the assigned URL should be running Carrier Owl.

If any changes to `zappa_settings.json` are made, the file should be re-encrypted before being committed. You can use the `openssl` invoke tasks to do this.
