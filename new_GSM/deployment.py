import os
from .settings import *
from .settings import BASE_DIR


ALLOWED_HOSTS = [os.environ["WEBSITE_HOSTNAME"]]

CSRF_TRUSTED_ORIGINS = [f"https://{os.environ["WEBSITE_HOSTNAME"]}"]

DEBUG = False

SECRET_KEY = os.environ["MY_SECRET_KEY"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_auth_adfs.middleware.LoginRequiredMiddleware",
]

# CORS_ALLOWED_ORIGINS 

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}


DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": os.getenv("server_name"),
        "USER": os.getenv("server_user"),
        "PASSWORD": os.getenv("server_password"),
        "HOST": os.getenv("server_host"),
        "PORT": os.getenv("server_port"),
        "OPTIONS": {
            "driver": "ODBC Driver 17 for SQL Server",
        },
    },
}


STATIC_ROOT = BASE_DIR/'staticfiles'
