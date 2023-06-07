from pathlib import Path
#Los settings para claves privadas
from . import local_settings
# solucion de rutas dinamicas y en este caso para solucionar el problema de 404 lector de archivos css y js
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ho6-z2h*&plasb@+spa0lrpzrr$$oht43o!p$hj17n#a!ioq*s'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'tfg',
    #mathfilters siver para realizar operaciones matematicas sencillas en el template
    #pip install django-mathfilters
    'mathfilters',
    # 'league'
    # 'rest_framework',
    #importado la app league
    'league.apps.LeagueConfig',
    #Forma parte de la app de legue y su informacion
    'django_cassiopeia',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #middleware remember me 
    'league.middleware.AutoLoginMiddleware'
]

ROOT_URLCONF = 'tfg.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # el lector de templates lo pongo manualmente
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

WSGI_APPLICATION = 'tfg.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = local_settings.DATABASES


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'Europe/Madrid'

USE_I18N = True
# variable para poder hacer las traducciones dinamicas
# LOCALE_PATHS = [
#     os.path.join(BASE_DIR, 'locale'),
# ]


USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Apartado de implementacion de la api


CASSIOPEIA_RIOT_API_KEY = local_settings.RIOT_API_KEY # api key in env var
CASSIOPEIA_DEFAULT_REGION = "EUW"   # default region
CASSIOPEIA_PIPELINE = {   # small pipeine to get started
    "Omnistone": {},
    "DDragon": {},
    "RiotAPI": {},
}

# IMAGENES ROOT
STATIC_URL = 'static/'
# Defninimos la direccion, esto es para arreglar el error de no lectura de css y de js
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL='media/'


# email registration validation
# backend   
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host de email 
EMAIL_HOST = 'smtp.gmail.com'
# email de la empresa   
EMAIL_HOST_USER = local_settings.EMAIL_HOST_USER
# password de la empresa   
EMAIL_HOST_PASSWORD = local_settings.EMAIL_HOST_PASSWORD
# puerto 
EMAIL_PORT = 587
EMAIL_USE_TLS = True

