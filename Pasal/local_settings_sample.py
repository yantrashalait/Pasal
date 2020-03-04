import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = ''

ALLOWED_HOSTS = []
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'database': 'pasal',
            'user': 'sanip',
            'password': 'Anku21dam',
        },
    }
}

LOGOUT_REDIRECT_URL = '/login/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# uncomment below in development
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# use in deployment
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
