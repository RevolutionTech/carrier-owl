"""
WSGI config for carrier_owl project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import cbsettings
from dotenv import load_dotenv


load_dotenv()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carrier_owl.settings")
cbsettings.configure("carrier_owl.settings.switcher")

application = get_wsgi_application()
