from .base import *
import os

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-dev-key")
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "trackstage"),
        "USER": os.environ.get("DB_USER", "trackstage"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "6432"),
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
