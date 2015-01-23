"""
Django settings for songrhyme project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
BASE_DIR = PROJECT_ROOT  # used by stock management commands

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'kasdlibneipbn9-9249hoinslknv,knae;nmglknae;'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
TEMPLATE_DIRS = (
        os.path.join(PROJECT_ROOT, 'templates'),
    )

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.Account'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_extensions',
    #'debug_toolbar',
    'djangular',
    'djangobower',
    'pipeline',
    'rest_framework.authtoken',
    'authemail',
    'compressor',

    'rhyme',
    'accounts',
)

BOWER_INSTALLED_APPS = (
    'jquery',
    'angular',
    'angular-resource',
    'angular-sanitize',
    'angular-route',
    'bootstrap',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'songrhyme',
        'PASSWORD': 'copters',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
BOWER_COMPONENTS_ROOT = STATIC_ROOT
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
    'djangobower.finders.BowerFinder',
)

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yui.YUICompressor'
PIPELINE_YUI_BINARY = '/opt/comms/bin/yuicompressor'

PIPELINE_JS = {
    'songrhyme': {
        'source_filenames': (
            #'js/lib/angular-strap.js',
            #'js/main.js',
            #'js/chartomatic.js',
            #'js/app/app.js',
            #'js/app/filters.js',
            #'js/app/controllers/controller.js',
            #'js/app/controllers/filter.js',
            #'js/app/services/service.js',
            #'js/app/services/objects.js',
            #'js/app/services/shared.js',
        ),
        'output_filename': 'js/songrhyme.js',
    }
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/django.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    #'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
    #'PAGINATE_BY': 10
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# Email settings for authemail
DEFAULT_EMAIL_FROM = 'songrhyme1@gmail.com'
DEFAULT_EMAIL_BCC = ''

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'songrhyme1@gmail.com'
EMAIL_HOST_PASSWORD = 'qyfoqnlmqwmhvskb'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
SERVER_EMAIL = 'songrhyme1@gmail.com'

from .local_settings import *
