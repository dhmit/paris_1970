"""

Production settings for dhmit/paris_1970

"""

from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']  # set in venv activate

ADMINS = [
    ('Ryaan Ahmed', 'rahmed@mit.edu')
]

ALLOWED_HOSTS = [
    'paris1970.dhmit.xyz',
    'paris1970.dhlab.mit.edu',
]

CORS_ORIGIN_WHITELIST = []

pw_path = Path(PROJECT_ROOT, 'db_password.txt')
with open(pw_path, 'r', encoding='utf-8') as pw_file:
    db_pw = pw_file.readline().strip()

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql',
         'HOST': 'paris1970-urop-fa22.crdpmszp71qh.us-east-1.rds.amazonaws.com',
         'USER': 'postgres',
         'NAME': 'paris1970-urop-fa22',
         'PORT': '5432',
         'PASSWORD': db_pw,
    }
}
