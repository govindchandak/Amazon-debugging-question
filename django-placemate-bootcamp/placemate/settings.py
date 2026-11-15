"""PlaceMate: campus placement portal (practice project for the Amazon debugging round)."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'placemate-practice-only'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'accounts',
    'drives',
    'applications',
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'accounts.middleware.token_auth_middleware',
]

ROOT_URLCONF = 'placemate.urls'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
TIME_ZONE = 'Asia/Kolkata'
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
