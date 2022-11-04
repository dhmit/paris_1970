"""

Local development Django settings for dhmit/paris_1970

Under no circumstances run the server with these settings in production!

This settings file is for running the remote DB with superuser privileges.

Only DH staff have these credentials. Ask Ryaan or Jeffrey if you think you need to use this.

"""


from .dev import *  # pylint: disable=unused-wildcard-import, wildcard-import

pw_path = Path(PROJECT_ROOT, 'remote_db_superuser_password.txt')
with open(pw_path, 'r', encoding='utf-8') as pw_file:
    db_pw = pw_file.readline().strip()

DATABASES['default']['USER'] = 'postgres'
DATABASES['default']['PASSWORD'] = db_pw

