"""

Local development Django settings for dhmit/paris_1970

Under no circumstances run the server with these settings in production!

Running with settings file lets you run with a local sqlite3 db instead
of our shared remote development database. Useful if you're doing something
that needs to interact with the Django admin panel, or if you're working
on db migrations.

"""


from .dev import *  # pylint: disable=unused-wildcard-import, wildcard-import

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BACKEND_DIR, 'db.sqlite3'),
    }
}
