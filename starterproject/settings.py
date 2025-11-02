"""
Django settings for starterproject project.
"""

from pathlib import Path
import os
from datetime import timedelta
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f3pm&hh)6iv-v$&-23#4b($m-ijvkm+xp(c1ibb4eq53ch7ufy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition
INSTALLED_APPS = [
    "inventory_finance",
    "transactions",
    "products",
    "contacts",
    "phonenumber_field",
    'cms',
    'filehandler',
    'solo',
    'books',
    'globalapp',
    'ckeditor',
    'users',
    'des',
    'simple_history',
    'drf_spectacular',
    "corsheaders",
    'wkhtmltopdf',
    'unfold',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'django_seed',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'starterproject.urls'

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = 'starterproject.wsgi.application'


# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myprojectdb',          # from AWS
        'USER': 'postgres',          # from AWS
        'PASSWORD': 'Pa$$w0rd!',     # from AWS
        'HOST': 'database-1.cto6c2c8g0z4.ap-southeast-2.rds.amazonaws.com',  # from AWS RDS
        'PORT': '5432',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ✅ Static & Media Settings
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   # collectstatic output

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # development static files
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/upload/'
MEDIA_ROOT = BASE_DIR / 'upload'


# Custom User
AUTH_USER_MODEL = 'users.Users'

# CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 5,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

# JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
}

# drf-spectacular
SPECTACULAR_SETTINGS = {
    'TITLE': 'Management Admin API',
    'DESCRIPTION': 'Your project description',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False,
}

PHONENUMBER_DEFAULT_REGION = 'US'

# Email Backend
EMAIL_BACKEND = 'des.backends.ConfiguredEmailBackend'

# wkhtmltopdf config
WKHTMLTOPDF_PATH = '/path/to/wkhtmltopdf'
os.environ["PATH"] += os.pathsep + os.path.dirname(WKHTMLTOPDF_PATH)

# Unfold Admin UI
UNFOLD = {
    "SITE_TITLE": "Management Super Admin",
    "SITE_HEADER": "Management Super Admin",
    "SITE_BRAND": "Your Brand",
    "USE_THEME": True,
    "SITE_DROPDOWN": [
        {
            "icon": "list",
            "title": _("Activity Log"),
            "link": reverse_lazy("admin:activity-log"),
        },
    ]
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

