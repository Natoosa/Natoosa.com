'''Use this for production'''

from .base import *

DEBUG = False

ALLOWED_HOSTS += ["localhost",'www.natoosa.com','natoosa.com']
WSGI_APPLICATION = 'home.wsgi.application'

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'natoosa_com_N91rjQ3M',
    'USER': 'natoosacomeUsV',
    'PASSWORD': '5LSuZfagEbhweKzj9vCkGiRN',
    'HOST': 'localhost',
    'PORT': '3306',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



