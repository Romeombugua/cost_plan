import sys
from pathlib import Path

# Base directory of the Django project (webapp/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Root of the cost_plan project (parent of webapp/) — needed to import docling_extract
COSTPLAN_ROOT = BASE_DIR.parent
if str(COSTPLAN_ROOT) not in sys.path:
    sys.path.insert(0, str(COSTPLAN_ROOT))

# torch must be imported before any transformers/Qt import on Windows
import torch  # noqa: F401

SECRET_KEY = "django-insecure-costplan-dev-key-change-in-production"

DEBUG = True

ALLOWED_HOSTS = ["*"]
CSRF_TRUSTED_ORIGINS = ['https://extractor.adw.dev']

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "extractor",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "costplan_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "costplan_site.wsgi.application"

# No database models used
DATABASES = {}

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Media / upload directory
MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# NRM database default location (cost_plan root)
NRM_DB_DEFAULT = COSTPLAN_ROOT / "nrm_db.xlsx"
