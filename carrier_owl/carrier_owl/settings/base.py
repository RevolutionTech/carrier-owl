"""
Django settings for carrier_owl project.

"""

import os

from cbsettings import DjangoDefaults
import dj_database_url


class BaseSettings(DjangoDefaults):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    SECRET_KEY = os.environ['CARRIER_OWL_SECRET_KEY']
    DEBUG = True
    ALLOWED_HOSTS = []

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'social_django',
        'gcalendar.apps.GcalendarConfig',
        'event.apps.EventConfig',
    ]
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
    ROOT_URLCONF = 'carrier_owl.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    WSGI_APPLICATION = 'carrier_owl.wsgi.application'

    # Database
    DATABASES = {
        'default': dj_database_url.config(
            env='CARRIER_OWL_DATABASE_URL',
            default='postgres://postgres@localhost/carrier_owl'
        ),
    }

    # Authentication
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]
    AUTHENTICATION_BACKENDS = [
        'social_core.backends.google.GoogleOAuth2',
        'django.contrib.auth.backends.ModelBackend',
    ]
    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
        'social_core.pipeline.social_auth.associate_by_email',
    )
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['CARRIER_OWL_GOOGLE_OAUTH2_CLIENT_ID']
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['CARRIER_OWL_GOOGLE_OAUTH2_CLIENT_SECRET']
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['https://www.googleapis.com/auth/calendar.events']
    SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'access_type': 'offline'}
    LOGIN_REDIRECT_URL = '/admin/'

    # Internationalization
    TIME_ZONE = 'UTC'
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'

    # Google Calendar
    GCALENDAR_EVENT_TIMEZONE = 'America/Los_Angeles'

    # Event details
    EVENT_WEEKDAY = int(os.environ['CARRIER_OWL_EVENT_WEEKDAY'])
    EVENT_START_HOUR = int(os.environ['CARRIER_OWL_EVENT_START_HOUR'])
    EVENT_START_MINUTE = int(os.environ['CARRIER_OWL_EVENT_START_MINUTE'])
    EVENT_END_HOUR = int(os.environ['CARRIER_OWL_EVENT_END_HOUR'])
    EVENT_END_MINUTE = int(os.environ['CARRIER_OWL_EVENT_END_MINUTE'])
    EVENT_SUMMARY = os.environ['CARRIER_OWL_EVENT_SUMMARY']
    EVENT_DESCRIPTION = os.environ.get('CARRIER_OWL_EVENT_DESCRIPTION')
    EVENT_LOCATION = os.environ.get('CARRIER_OWL_EVENT_LOCATION')
    EVENT_ATTENDEES = os.environ.get('CARRIER_OWL_EVENT_ATTENDEES', '').split(',')
