# nopycln: file
from .settings import (
    AUTH_USER_MODEL,
    BASE_DIR,
    INSTALLED_APPS,
    REST_FRAMEWORK,
    ROOT_URLCONF,
    SECRET_KEY,
    USE_TZ,
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
