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


SITE_ID = 1

ALLOWED_HOSTS = []  # wildcard

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]
