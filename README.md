# Carrier Owl
#### Assistant for sending out personalized invitations

## Deprecated

This project is no longer being maintained by the owner.

---

![CI](https://github.com/RevolutionTech/carrier-owl/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/RevolutionTech/carrier-owl/branch/main/graph/badge.svg)](https://codecov.io/gh/RevolutionTech/carrier-owl)

## Setup

### Installation

Use [poetry](https://github.com/sdispater/poetry) to install Python dependencies:

    poetry install

### Configuration

Carrier Owl reads in environment variables from your local `.env` file. See `.env-sample` for configuration options. Be sure to [generate your own secret key](http://stackoverflow.com/a/16630719).

With everything installed and all files in place, you may now create the database tables. You can do this with:

    poetry run python manage.py migrate
