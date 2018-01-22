"""
Django settings for carrier_owl project.

"""

from cbsettings import switcher

from carrier_owl.settings.base import BaseSettings


switcher.register(BaseSettings)
