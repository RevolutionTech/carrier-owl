"""
Django settings for carrier_owl project.

"""

import os
from distutils.util import strtobool

from cbsettings import DjangoDefaults


def aws_s3_bucket_url(settings_class, bucket_name_settings):
    bucket_name = getattr(settings_class, bucket_name_settings, "")
    if bucket_name:
        return f"https://{bucket_name}.s3.amazonaws.com"
    return ""


class BaseSettings(DjangoDefaults):

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    SECRET_KEY = os.environ["CARRIER_OWL_SECRET_KEY"]
    DEBUG = True
    ALLOWED_HOSTS = []

    # Application definition
    INSTALLED_APPS = [
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "zappa_django_utils",
        "django_s3_storage",
        "social_django",
        "gcalendar.apps.GcalendarConfig",
        "event.apps.EventConfig",
        "emails.apps.EmailsConfig",
    ]
    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]
    ROOT_URLCONF = "carrier_owl.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ]
            },
        }
    ]
    WSGI_APPLICATION = "carrier_owl.wsgi.application"

    # Database
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

    # Authentication
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]
    AUTHENTICATION_BACKENDS = [
        "social_core.backends.google.GoogleOAuth2",
        "django.contrib.auth.backends.ModelBackend",
    ]
    SOCIAL_AUTH_PIPELINE = (
        "social_core.pipeline.social_auth.social_details",
        "social_core.pipeline.social_auth.social_uid",
        "social_core.pipeline.social_auth.social_user",
        "social_core.pipeline.user.get_username",
        "social_core.pipeline.user.create_user",
        "social_core.pipeline.social_auth.associate_user",
        "social_core.pipeline.social_auth.load_extra_data",
        "social_core.pipeline.user.user_details",
        "social_core.pipeline.social_auth.associate_by_email",
    )
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ["CARRIER_OWL_GOOGLE_OAUTH2_CLIENT_ID"]
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ[
        "CARRIER_OWL_GOOGLE_OAUTH2_CLIENT_SECRET"
    ]
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        "https://www.googleapis.com/auth/calendar.events"
    ]
    SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {"access_type": "offline"}
    LOGIN_REDIRECT_URL = "/admin/"

    # Internationalization
    TIME_ZONE = "UTC"
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    AWS_S3_KEY_PREFIX_STATIC = "static"
    AWS_S3_BUCKET_AUTH = False
    AWS_S3_MAX_AGE_SECONDS = 60 * 60 * 24 * 365  # 1 year

    @property
    def STATIC_URL(self):
        return "{aws_s3}/{static}/".format(
            aws_s3=aws_s3_bucket_url(self, "AWS_S3_BUCKET_NAME_STATIC"),
            static=self.AWS_S3_KEY_PREFIX_STATIC,
        )

    # Google Calendar
    GCALENDAR_EVENT_TIMEZONE = "America/Los_Angeles"

    # Email
    EMAIL_HOST = os.environ["CARRIER_OWL_EMAIL_HOST"]
    EMAIL_PORT = os.environ.get("CARRIER_OWL_EMAIL_PORT", 25)
    EMAIL_HOST_USER = os.environ["CARRIER_OWL_EMAIL_USER"]
    EMAIL_HOST_PASSWORD = os.environ["CARRIER_OWL_EMAIL_PASSWORD"]
    EMAIL_USE_TLS = strtobool(os.environ.get("CARRIER_OWL_EMAIL_USE_TLS", "false"))

    def DEFAULT_FROM_EMAIL(self):
        return os.environ.get("CARRIER_OWL_EMAIL_FROM", self.EMAIL_HOST_USER)

    # Experimental switches
    EXPERIMENT_ADD_ATTENDEES_TO_EVENT = strtobool(
        os.environ.get("CARRIER_OWL_EXPERIMENT_ADD_ATTENDEES_TO_EVENT", "true")
    )
    EXPERIMENT_SEND_ATTENDEES_INVITATION_EMAIL = strtobool(
        os.environ.get("CARRIER_OWL_EXPERIMENT_SEND_ATTENDEES_INVITATION_EMAIL", "true")
    )
