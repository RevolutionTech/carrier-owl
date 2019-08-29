"""
Django settings for carrier_owl project.

"""

import os

from cbsettings import switcher

from carrier_owl.settings.base import BaseSettings
from carrier_owl.settings.prod import ProdSettings


api_gateway_stage = os.environ.get('STAGE', 'dev')
switcher.register(BaseSettings, api_gateway_stage == 'dev')
switcher.register(ProdSettings, api_gateway_stage == 'production')
