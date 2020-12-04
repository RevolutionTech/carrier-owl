"""
Django settings for carrier_owl project.

"""

import os

from configurations import Configuration, values


def aws_s3_bucket_url(settings_class, bucket_name_settings):
    bucket_name = getattr(settings_class, bucket_name_settings, "")
    if bucket_name:
        return f"https://{bucket_name}.s3.amazonaws.com"
    return ""


class BaseConfig(Configuration):

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    SECRET_KEY = values.SecretValue(environ_prefix="CARRIER_OWL")
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
        "django_s3_sqlite",
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
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = values.SecretValue(
        environ_name="GOOGLE_OAUTH2_CLIENT_ID", environ_prefix="CARRIER_OWL"
    )
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = values.SecretValue(
        environ_name="GOOGLE_OAUTH2_CLIENT_SECRET", environ_prefix="CARRIER_OWL"
    )
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
    EMAIL_HOST = values.SecretValue(environ_prefix="CARRIER_OWL")
    EMAIL_PORT = values.IntegerValue(25, environ_prefix="CARRIER_OWL")
    EMAIL_HOST_USER = values.SecretValue(
        environ_name="EMAIL_USER", environ_prefix="CARRIER_OWL"
    )
    EMAIL_HOST_PASSWORD = values.SecretValue(
        environ_name="EMAIL_PASSWORD", environ_prefix="CARRIER_OWL"
    )
    EMAIL_USE_TLS = values.BooleanValue(False, environ_prefix="CARRIER_OWL")
    DEFAULT_FROM_EMAIL = values.Value(
        EMAIL_HOST_USER, environ_name="EMAIL_FROM", environ_prefix="CARRIER_OWL"
    )


class ProdConfig(BaseConfig):

    DEBUG = False
    ALLOWED_HOSTS = ["masonic.games"]

    # Database
    DATABASES = {
        "default": {
            "ENGINE": "django_s3_sqlite",
            "NAME": "db.sqlite3",
            "BUCKET": "carrier-owl-sqlite3",
        }
    }

    # Static files
    STATICFILES_STORAGE = "django_s3_storage.storage.ManifestStaticS3Storage"
    AWS_S3_BUCKET_NAME_STATIC = "carrier-owl"

    AWS_ACCESS_KEY_ID = values.SecretValue(environ_prefix="CARRIER_OWL")
    AWS_SECRET_ACCESS_KEY = values.SecretValue(environ_prefix="CARRIER_OWL")


# Config for running ./manage.py collectstatic
# without requiring secrets that are unused by the command
class ProdCollectStaticConfig(ProdConfig):

    SECRET_KEY = "dummyvalue"
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "dummyvalue"
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "dummyvalue"
    EMAIL_HOST = "dummyvalue"
    EMAIL_HOST_USER = "dummyvalue"
    EMAIL_HOST_PASSWORD = "dummyvalue"
