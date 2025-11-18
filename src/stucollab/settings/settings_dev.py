import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

#Local
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gzd(#lhs7eg@r$nx_wfp$n-$ad7yfhpgz(gvlyd_!o(l3$lg+t'


# SECURITY WARNING: don't run with debug turned on in production!
#Local
DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Application definition

INSTALLED_APPS = [
    'storages',
    'users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'groups',
    'collab',
    'base',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stucollab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates", ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stucollab.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

#Local

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stucollab',
        'USER': 'math',
        'PASSWORD': 'P0$t9r&$q1',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

#Local
# Configuration MinIO (Django 4.2+)

STORAGES = {
    "default": {
        "BACKEND":
"storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key":
"OXP4pAEc4CQTY05i8vhP",
            "secret_key":
"LM3CnPl4Fcnaqcqj4NOJsg6Nu5cfMCCp2gGb8zJx",
            "bucket_name":
"stucollab",
            "endpoint_url":
"http://localhost:9000",
            "region_name":
"us-east-1",
            "signature_version":
"s3v4",
            "use_ssl": False,
            "querystring_auth":
True,
        },
    },
    "staticfiles": {
        "BACKEND":
"django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = "users.User"

LOGIN_URL = "/me/signin_signup"



# Pour le développement (affiche les emails dans la console)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = 'stucollab.app@gmail.com'
