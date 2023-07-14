"""

Local development Django settings for dhmit/paris_1970

Under no circumstances run the server with these settings in production!

"""


from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qqucn931x78rx054n(6g(s_3vxppjw$f24e(9&v6rsbd0&0$2e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SITE_ID = 1

ALLOWED_HOSTS = []  # wildcard

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
        'db_queries': {
            'format': '\nDB Query - %(asctime)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'console_db': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'db_queries'
        },
    },
    # Comment me in to get database query logging in the console.
    #'loggers': {
    #    'django.db.backends': {
    #        'level': 'DEBUG',
    #        'handlers': ['console_db'],
    #        'propagate': False,
    #    },
    #},
}
