

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "ou6)v2_&m7_$f-qt*r%db3d1_vs)@4)7qmh**w(ne9gvoe3*h6"

DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"


LB_IP = os.environ.get("DJANGO_LB_IP", "34.117.8.0")
ALLOWED_HOSTS = ['*', 'akshith.app', 'unimarketplace.akshith.app']

CSRF_TRUSTED_ORIGINS = [
    f"http://{LB_IP}",
    f"https://{LB_IP}",
    f"https://{LB_IP}:443",
    "http://akshith.app",
    'https://akshith.app',
    'https://unimarketplace.akshith.app',
]



CSRF_COOKIE_SECURE    = False
SESSION_COOKIE_SECURE = False


CSRF_COOKIE_SAMESITE    = None  
SESSION_COOKIE_SAMESITE = None  

SECURE_SSL_REDIRECT = False


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
    "rest_framework",
    "storages",
]

MIDDLEWARE = [
   # "app1.middleware.HTTPSRedirectMiddleware",
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


# ——— Database ———
DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",

        "NAME":     os.environ["DB_NAME"],
        "USER":     os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST":     os.environ.get("DB_HOST", "34.168.133.231"),
        "PORT":     os.environ.get("DB_PORT", "5432"),
    }
}
# … rest of your settings …

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "app1" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL  = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME       =  "planar-outlook-454509-e8-bucket-1"  
GS_LOCATION          = "media"
GS_QUERYSTRING_AUTH  = False
MEDIA_URL            = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/{GS_LOCATION}/"

LOGIN_URL           = "/login/"
LOGIN_REDIRECT_URL  = "/"
LOGOUT_REDIRECT_URL = "/"
DEFAULT_AUTO_FIELD  = "django.db.models.BigAutoField"
