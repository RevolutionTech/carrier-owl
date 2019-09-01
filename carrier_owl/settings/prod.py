import os

from carrier_owl.settings.base import BaseSettings


class ProdSettings(BaseSettings):

    DEBUG = False
    ALLOWED_HOSTS = ["masonic.games"]

    # Database
    DATABASES = {
        "default": {
            "ENGINE": "zappa_django_utils.db.backends.s3sqlite",
            "NAME": "db.sqlite3",
            "BUCKET": "carrier-owl-sqlite3",
        }
    }

    # Static files
    STATICFILES_STORAGE = "django_s3_storage.storage.ManifestStaticS3Storage"
    AWS_S3_BUCKET_NAME_STATIC = "carrier-owl"

    @property
    def AWS_ACCESS_KEY_ID(self):
        return os.environ["CARRIER_OWL_AWS_ACCESS_KEY_ID"]

    @property
    def AWS_SECRET_ACCESS_KEY(self):
        return os.environ["CARRIER_OWL_AWS_SECRET_ACCESS_KEY"]
