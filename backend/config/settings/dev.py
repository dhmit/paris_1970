"""

Local development Django settings for dhmit/paris_1970

Under no circumstances run the server with these settings in production!

"""

from .base import *  # pylint: disable=unused-wildcard-import, wildcard-import


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'qqucn931x78rx054n(6g(s_3vxppjw$f24e(9&v6rsbd0&0$2e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []  # wildcard
<<<<<<< Updated upstream
=======

# cms
SITE_ID = 1

LANGUAGES = [
    ('en', 'English'),
    ('de', 'German'),
]

X_FRAME_OPTIONS = 'SAMEORIGIN'

CMS_TEMPLATES = [
    ('homepage.html', 'Home page template'),
    ('blog_post.html', 'Blog page template')
]

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

CMS_PERMISSION = True
CMS_TOOLBAR_ANONYMOUS_ON = True
>>>>>>> Stashed changes
