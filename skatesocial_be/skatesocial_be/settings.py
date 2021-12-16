import os
import datetime
from datetime import timedelta
from pathlib import Path
from unipath import Path as unipathPath
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

SECRET_KEY = env("DJANGO_SECRET_KEY")
ENV_TYPE = env("DJANGO_ENVIRONMENT")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if ENV_TYPE in ["local", "dev"] else False

SITE_ID = 1

if ENV_TYPE in ["local", "dev"]:
    SITE_ADDRESS = "http://localhost:8000"
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
elif ENV_TYPE == "prod":
    SITE_ID = 1
    SECURE_SSL_REDIRECT = True
    SITE_ADDRESS = "www.oldiesinanotherroom.com"  # change me, obviously
    EMAIL_BACKEND = (
        "django.core.mail.backends.console.EmailBackend"  # change me, obviously
    )
SITE_URL = SITE_ADDRESS
# SERVER_HOSTNAME = env('SERVER_HOSTNAME')
ALLOWED_HOSTS = ["127.0.0.1:8000", "127.0.0.1", "localhost", SITE_ADDRESS]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.gis",
]
INSTALLED_APPS += [
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "dj_rest_auth",  # https://github.com/iMerica/dj-rest-auth
    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html
    "rest_framework_simplejwt",
    "django_countries",
]

INSTALLED_APPS += [
    "crew_network",
    "skate_spots",
    # "skate_dates",
]
# TODO: https://github.com/venits/react-native-map-clustering
# maybe https://openbase.com/js/react-native-open-maps
# maybe https://openbase.com/js/react-native-google-place-picker

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "skatesocial_be.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # os.path.join(BASE_DIR, 'templates'),
            # os.path.join(BASE_DIR, 'templates', 'industry'),
        ],
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

WSGI_APPLICATION = "skatesocial_be.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.mysql",
        "NAME": env("MYSQL_NAME"),
        "USER": env("MYSQL_USER"),
        "PASSWORD": env("MYSQL_PASSWORD"),
        # "PORT": int(env("MYSQL_PORT", 3306)),
        "HOST": env("MYSQL_HOST"),
        "OPTIONS": {
            "sql_mode": "TRADITIONAL",
            "charset": "utf8",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
        # "rest_framework.authentication.SessionAuthentication", Removed so don't need csrf tokens, which are unnecessary if don't use browser
        "rest_framework.authentication.BasicAuthentication",
    ],
}
REST_AUTH_SERIALIZERS = {
    # "USER_LOGIN_SERIALIZER": "auth.api.serializers." "LoginSuccessSerializer",
    "USER_DETAILS_SERIALIZER": "auth.api.serializers."
    "UserBasicSerializer",
}
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# # Reminder: edit the files in STATICFILES_DIRS. the ones in static are auto generated.
STATICFILES_DIRS = [os.path.join(BASE_DIR, "staticfiles")]

BASE_DIR = unipathPath(__file__).ancestor(3)
TEMPLATE_DIRS = (BASE_DIR.child("templates"),)


STATIC_URL = "/static/"
MEDIA_URL = "/media/"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=365 * 10),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=365 * 10),
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}
