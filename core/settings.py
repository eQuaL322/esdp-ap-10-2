"""
Django's settings for core project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-znfdq*e7&rjk2rn1oxh9g@v)ln=8vynzfnop+zj+qmi80k2@)3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

if os.environ.get("ALLOWED_HOSTS") is not None:
    try:
        ALLOWED_HOSTS += os.environ.get("ALLOWED_HOSTS").split(",")
    except Exception as e:
        print("Cant set ALLOWED_HOSTS, using default instead")

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_bootstrap5',
    'accounts',
    'KaifSchool',
    'chat',
    'phonenumber_field',
    'phonenumbers',
    'django_initials_avatar',
    'django_json_widget',
    'django_bootstrap_icons',
    'sorl.thumbnail',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
load_dotenv()
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "kaifschool",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "db",
        "PORT": '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGES = [
    ('ru', _('Russian')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]
LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "/static/")
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'

AUTH_USER_MODEL = 'accounts.Account'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INITIALS_AVATAR_BG_COLORS = [
    "#E284B3", "#FFED8B", "#681313", "#F3C1C6", "#735372", "#009975", "#FFBD39", "#B1E8ED", "#52437B", "#F76262",
    "#216583", "#293462", "#DD9D52", "#936B93", "#6DD38D", "#888888", "#6F8190", "#BCA0F0", "#AAF4DD", "#96C2ED",
    "#3593CE", "#5EE2CD", "#96366E", "#E38080"
]

INITIALS_AVATAR_TEXT_COLOR = '#fff'
INITIALS_AVATAR_TEXT_LENGTH = 2
INITIALS_AVATAR_WIDTH = 45
INITIALS_AVATAR_HEIGHT = 45
INITIALS_AVATAR_FONT_SIZE = 20
INITIALS_AVATAR_ROUNDED = False
INITIALS_AVATAR_CAPITALIZE = True
INITIALS_AVATAR_LOWERCASE = False
INITIALS_AVATAR_BOLD = False
INITIALS_AVATAR_CACHE_TIMEOUT = 45 * 45

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'kaifschoola@gmail.com'
EMAIL_HOST_PASSWORD = 'zgsjrpiagmfihihe'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SUPPORT_EMAIL = 'kaifschoola@gmail.com'

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'