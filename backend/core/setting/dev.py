from core.settings import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY", default="unsafe-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)


# ALLOWED_HOSTS = []
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=['0.0.0.0', '127.0.0.1'])

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]


INTERNAL_IPS = [
    "127.0.0.1",
]

# sites
SITE_ID = 2

# using this in development mode
# we use smtp service in production mode
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
