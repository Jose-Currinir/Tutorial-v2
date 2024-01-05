import json
import os
from pathlib import Path
import environ
from dotenv import load_dotenv
import dj_database_url
from google.oauth2 import service_account


load_dotenv()
env = environ.Env()
environ.Env.read_env()
ENVIRONMENT = env


BASE_DIR = Path(__file__).resolve().parent.parent
#SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-jnd42709vnsx33g@_5w+3&r5f2*z^a)-y71st-q*#86n$#x#%8')
SECRET_KEY = os.environ.get('SECRET_KEY')
SITE_NAME = 'Primera CBPA'
#DEBUG = os.environ.get('DEBUG')
DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1"
]
if not DEBUG:
    ALLOWED_HOSTS = [
        "primeracbpa.cl",
        ".primeracbpa.cl",
        "www.primeracbpa.cl"
    ]

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

DJANGO_APPS = [
    'django_dump_load_utf8',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
PROJECT_APPS = [
    'apps.webpage',
    #'apps.inventory'
]
THIRD_PARTY_APPS = [
    'bootstrap5',
    'storages',
]
INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'primera.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'primera.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://primera_2h6q_user:DHSdSk3rHI0Shijij88QkV1QMIaTr68v@dpg-cm2qfcda73kc73elip60-a/primera_2h6q',
        conn_max_age=600
    )
}


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
# Lenguaje y zona
LANGUAGE_CODE = 'es-CL'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

# Archivos estaticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    #STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Archivos media
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
FILE_UPLOAD_PERMISSIONS = 0o640

EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'


if not DEBUG:
    GS_BUCKET_NAME = 'primeracbpa-dev'
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    credenciales_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if credenciales_json:
        credenciales_dict = json.loads(credenciales_json)
        GS_CREDENTIALS = service_account.Credentials.from_service_account_info(credenciales_dict)
    else:
        GS_CREDENTIALS = None
        GS_CREDENTIALS = service_account.Credentials.from_service_account_info(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))