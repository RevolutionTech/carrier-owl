#!/usr/bin/env python
import os
import sys

from dotenv import load_dotenv


if __name__ == "__main__":
    load_dotenv()

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "carrier_owl.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "BaseConfig")
    try:
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import django-configurations. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
