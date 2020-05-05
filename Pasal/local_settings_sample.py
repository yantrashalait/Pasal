import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = os.environ.get('SECRET_KEY', 'zhg-y4#7j-d*p-__@j#*3z@!y24fz8%^z2v6atuy4bo9vlrv_j')

# specify the domain names in the allowed_hosts list.
# For example: 
# ALLOWED_HOSTS = ['www.example.com', 'example.com']
ALLOWED_HOSTS = []

# set Debug = False in deployment
DEBUG = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'database': '',
            'user': '',
            'password': '',
        },
    }
}

LOGOUT_REDIRECT_URL = '/login/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# uncomment below in development and comment in deployment
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# uncomment in deployment
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
