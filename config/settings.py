"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
#from django.utils.crypto import get_random_string
from django.core.management.utils import get_random_secret_key
import os

USER_MANAGEMENT = os.environ.get('USER_MANAGEMENT') == '1'
DEMO = os.environ.get('DEMO') == '1'
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_random_secret_key()
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == '1'

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://*').split(',')
# CSRF_TRUSTED_ORIGINS = list(os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://*'))
INTERNAL_IPS = [
    "127.0.0.1",
]
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
SESSION_ENGINE = "django.contrib.sessions.backends.db"
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'huey.contrib.djhuey',

    'core.apps.CoreConfig',
    'translator.apps.TranslatorConfig',
    'encrypted_model_fields', # must set FIELD_ENCRYPTION_KEY value
]
DEBUG_PLUGINS = [
    "debug_toolbar",
    'bx_django_utils',  # https://github.com/boxine/bx_django_utils
    'huey_monitor',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
DEBUG_MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]
if DEBUG:
    INSTALLED_APPS += DEBUG_PLUGINS
    MIDDLEWARE += DEBUG_MIDDLEWARE


ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATA_FOLDER = BASE_DIR / "data"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": DATA_FOLDER / "db.sqlite3",
    }
}

HUEY = {
    'huey_class': 'huey.SqliteHuey',
    'filename': DATA_FOLDER / "huey.sqlite3",
    'consumer': {
        'workers': 1,
        'worker_type': 'thread',
    },
    "immediate": False,
}
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
LOCALE_PATHS = [BASE_DIR / "locale"]


TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#https://pypi.org/project/django-encrypted-model-fields/
FIELD_ENCRYPTION_KEY = "RWdGiEq3LgOf3Tyt3ALlEnxUkIlL4wS2dCDBe_sLWWo="

TRANSLATION_LANGUAGES = [
   ("English", "English"),
   ("Chinese Simplified", "Chinese Simplified"),
   ("Chinese Traditional", "Chinese Traditional"),
   ("Russian", "Russian"),
   ("Japanese", "Japanese"),
   ("Korean", "Korean"),
   ("Czech", "Czech"),
   ("Danish", "Danish"),
   ("German", "German"),
   ("Spanish", "Spanish"),
   ("French", "French"),
   ("Indonesian", "Indonesian"),
   ("Italian", "Italian"),
   ("Hungarian", "Hungarian"),
   ("Norwegian Bokmal", "Norwegian Bokmal"),
   ("Dutch", "Dutch"),
   ("Polish", "Polish"),
   ("Portuguese", "Portuguese"),
   ("Swedish", "Swedish"),
   ("Turkish", "Turkish"),
]
LOG_LEVEL= "ERROR" if not DEBUG else "INFO"
LOGGING = {
   'version': 1,
   'disable_existing_loggers': False,
   'formatters':{
       'verbose':{
           'format': '{asctime} {message}',
           'style': '{',
           },
       },
   'handlers': {
       'logfile': {
           'level': LOG_LEVEL,
           'class': 'logging.handlers.RotatingFileHandler',
           'filename': DATA_FOLDER / 'app.log',
           'maxBytes': 1024 * 1024 * 10,  # 10 MB
           'encoding': 'utf-8',
           'formatter': 'verbose',
       },
   },
   'root': {
       'handlers': ['logfile'],
       'level': LOG_LEVEL,
   },
}
