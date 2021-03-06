"""
Django settings for cas project.

Generated by 'django-admin startproject' using Django 2.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(nh9$e905citn1me21e89al0(s^tb%1wdr$803(l4wp$7p_tv_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '*',
    '127.0.0.1',
]

# MAMA Settings
# MAMA_CAS_ALLOW_AUTH_WARN = True

# MAMA_CAS_ATTRIBUTE_CALLBACKS = ('path.to.custom_attributes',) # These are defined in the MAMA_CAS_SERVICES

# In a convenient location
def custom_attributes(user, service):
    return {
        'givenName': user.first_name, 
        'email': user.email
    }

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Custom
    'mama_cas',
    'main'
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

MAMA_CAS_ENABLE_SINGLE_SIGN_OUT = True

MAMA_CAS_FOLLOW_LOGOUT_URL = True

MAMA_CAS_SERVICES = [
    # STORM
    {
        'SERVICE': 'http://127.0.0.1:8000',
        'CALLBACKS': [
            'mama_cas.callbacks.user_name_attributes',
        ],
        'LOGOUT_ALLOW': True,
        'LOGOUT_URL': 'http://127.0.0.1:8000/callback/',
    },
    # Other Server
    {
        'SERVICE': 'http://127.0.0.1:2048',
        'CALLBACKS': [
            'mama_cas.callbacks.user_name_attributes',
        ],
        'LOGOUT_ALLOW': True,
        'LOGOUT_URL': 'http://127.0.0.1:2048/callback/',
    },
 ]

ROOT_URLCONF = 'cas.urls'

MAMA_CAS_LOGIN_TEMPLATE = os.path.join(BASE_DIR, 'templates/login.html')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'cas.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

if DEBUG:
   DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'cas',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432'
        }
   }
else: 
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_NAME'],
            'USER': os.environ['RDS_USER'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOST'],
            'PORT': '5432'
        },
        # 'original': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # }
    }

# CUSTOM USER MODEL
AUTH_USER_MODEL = 'main.User'

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

if DEBUG:

    STATIC_URL = '/static/'


STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
        #'/var/www/static/',
    ]