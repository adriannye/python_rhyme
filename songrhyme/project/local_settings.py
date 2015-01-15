# local_settings.py
DEBUG = True
DOMAIN = 'localhost:8000'
CACHE_BACKEND = 'locmem://'
NOSE_ARGS = ['--exclude-dir=third_party_libs']

DATABASES = {
    'default': {
        'NAME': 'songrhyme',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'PASSWORD': 'copters',
        'HOST': 'localhost',
    },
}
