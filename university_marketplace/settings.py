# settings.py

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "your-secret-key")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"


if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND         = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST            = "smtp.sendgrid.net"          # or your SMTP host
    EMAIL_PORT            = 587
    EMAIL_USE_TLS         = True
    EMAIL_HOST_USER       = "apikey"                     # for SendGrid use “apikey”
    EMAIL_HOST_PASSWORD   = os.environ.get("SENDGRID_API_KEY", "")
    DEFAULT_FROM_EMAIL    = "no‑reply@yourdomain.com"
    
ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [

    "https://localhost:8000",

    "http://localhost:8000",

    "https://127.0.0.1:8000",
    "http://127.0.0.1:8000",


    "https://supreme-barnacle-jjqjgqj66vwphpq4q-8000.app.github.dev",

    "https://*.app.github.dev",
    "https://*.run.app",
]



CSRF_COOKIE_SECURE      = True
CSRF_COOKIE_SAMESITE    = None
SESSION_COOKIE_SECURE   = True

SESSION_COOKIE_SAMESITE = None

USE_X_FORWARDED_HOST    = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",   
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "university_marketplace.app1.apps.App1Config",    
    "rest_framework"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",            
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "university_marketplace.urls"

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
                "university_marketplace.app1.context_processors.global_notifications",
            ],
        },
    },
]

WSGI_APPLICATION = "university_marketplace.wsgi.application"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}








STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / 'app1' / 'static',
]
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL  = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGIN_URL           = "/login/"
LOGIN_REDIRECT_URL  = "/"
LOGOUT_REDIRECT_URL = "/"
DEFAULT_AUTO_FIELD  = "django.db.models.BigAutoField"

