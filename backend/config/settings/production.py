"""

Production settings for dhmit/paris_1970

"""

from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# SECRET_KEY = os.environ['DJANGO_SECRET_KEY']  # set in venv activate

ADMINS = [('Ahmed', 'rahmed@mit.edu')]

ALLOWED_HOSTS = []

CORS_ORIGIN_WHITELIST = []
