from datetime import timedelta
from pathlib import Path
import os  # Importing the os module
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.x/howto/static-files/
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-o!rx1=snmqi1fr0&lav@%%i1tnl06)tfr2r#e!f@8zs9xg^nyh"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [".vercel.app", ".now.sh", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "djoser",
    "django_auth_adfs",
    "corsheaders",
    "adminsortable2",
    "test_app.apps.TestAppConfig",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_auth_adfs.middleware.LoginRequiredMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

ROOT_URLCONF = "new_GSM.urls"

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

WSGI_APPLICATION = "new_GSM.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres.lyuqhgdwngpcvdalryel",
        "PASSWORD": "GSM_CGT_247",
        "HOST": "aws-0-us-west-1.pooler.supabase.com",
        "PORT": 6543,
        "DISABLE_SERVER_SIDE_CURSORS": True,
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "GSM Local",
#         "USER": "postgres",
#         "PASSWORD": "qweqweqwe",
#         "HOST": "localhost",
#         "PORT": 5433,
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Toronto"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
# STATICFILES_URL = [BASE_DIR / "static"]
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_build", "static")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "django_auth_adfs.rest_framework.AdfsAccessTokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
}

DJOSER = {
    "SERIALIZERS": {
        "user_create": "core.serializers.UserCreateSerializer",
        "current_user": "core.serializers.UserSerializer",
    }
}

AUTHENTICATION_BACKENDS = ("django_auth_adfs.backend.AdfsAuthCodeBackend",)

# AUTH_ADFS = {
#     "SERVER": "adfs.yourcompany.com",
#     "CLIENT_ID": "your-configured-client-id",
#     "RELYING_PARTY_ID": "your-adfs-RPT-name",
#     # Make sure to read the documentation about the AUDIENCE setting
#     # when you configured the identifier as a URL!
#     "AUDIENCE": "microsoft:identityserver:your-RelyingPartyTrust-identifier",
#     "CA_BUNDLE": "/path/to/ca-bundle.pem",
#     "CLAIM_MAPPING": {
#         "first_name": "given_name",
#         "last_name": "family_name",
#         "email": "email",
#     },
# }
client_id = "43877c69-35ac-40ba-8b81-1d75c3aeff81"
client_secret = "Qqn8Q~hq4VQdUc~zo4AJQdHhZg8JUOZOhQClecsR"
tenant_id = "e500d90a-f722-4c6b-a5b8-6fda28cef811"

AUTH_ADFS = {
    "AUDIENCE": client_id,
    "CLIENT_ID": client_id,
    "CLIENT_SECRET": client_secret,
    "CLAIM_MAPPING": {
        "first_name": "given_name",
        "last_name": "family_name",
        "email": "upn",
    },
    "GROUPS_CLAIM": "roles",
    "MIRROR_GROUPS": True,
    "USERNAME_CLAIM": "upn",
    "TENANT_ID": tenant_id,
    "RELYING_PARTY_ID": client_id,
}


LOGIN_URL = "django_auth_adfs:login"
LOGIN_REDIRECT_URL = "/"
CUSTOM_FAILED_RESPONSE_VIEW = "dot.path.to.custom.views.login_failed"
