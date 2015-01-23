# local_settings.py
DEBUG = True
DOMAIN = 'localhost:8000'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

DATABASES = {
    'default': {
        'NAME': 'songrhyme',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'PASSWORD': 'copters',
        'HOST': 'localhost',
    },
}
