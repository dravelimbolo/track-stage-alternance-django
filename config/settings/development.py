from .base import *

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-dev-key")
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
