"""

Local development Django settings for dhmit/paris_1970

Under no circumstances run the server with these settings in production!

"""


from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qqucn931x78rx054n(6g(s_3vxppjw$f24e(9&v6rsbd0&0$2e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

pw_path = Path(PROJECT_ROOT, 'db_password.txt')
with open(pw_path, 'r', encoding='utf-8') as pw_file:
    db_pw = pw_file.readline().strip()

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'HOST': 'paris1970-urop-fa22.crdpmszp71qh.us-east-1.rds.amazonaws.com',
       'USER': 'urop',
       'NAME': 'paris1970-urop-fa22',
       'PORT': '5432',
       'PASSWORD': db_pw,
    }
}

# NOTE(ra): AWS RDS is down on 2022-09-09 during our first hack session,
# so we're patching in this temporary sqlite3 DB. We'll restore the original
# situation once it's back up.
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BACKEND_DIR, 'db.sqlite3'),
#     }
# }


SITE_ID = 1

ALLOWED_HOSTS = []  # wildcard

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]



# Logging


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
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console_db'],
            'propagate': False,
        },
    },
}
