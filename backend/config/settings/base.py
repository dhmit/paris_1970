"""
Django base settings for dhmit/paris_1970 project.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from pathlib import Path

CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKEND_DIR = os.path.dirname(CONFIG_DIR)
MIGRATIONS_DIR = os.path.join(os.path.dirname(CONFIG_DIR), 'app/migrations')
SETTINGS_DIR = os.path.join(CONFIG_DIR, 'settings')
DB_PATH = os.path.join(BACKEND_DIR, 'db.sqlite3')
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
BACKEND_DATA_DIR = os.path.join(BACKEND_DIR, 'data')
GOOGLE_TOKEN_FILE = os.path.join(BACKEND_DIR, 'token.pickle')
ANALYSIS_DIR = Path(PROJECT_ROOT, 'backend', 'app', 'analysis')
ANALYSIS_PICKLE_PATH = Path(BACKEND_DIR, ANALYSIS_DIR, 'analysis_results')
LOCAL_PHOTOS_DIR = "/static/images/photos"
LOCAL_PHOTOS_LOCATION = Path(PROJECT_ROOT, 'assets', 'images', 'photos')
PHOTOGRAPHERS_DIR = "/static/images/photographers"
TEST_PHOTOS_DIR = Path(PROJECT_ROOT, 'backend', 'data', 'test_photos')
TESSDATA_DIR = Path(PROJECT_ROOT, 'backend', 'data', 'tessdata')
TEXT_DETECTION_PATH = Path(BACKEND_DATA_DIR, 'frozen_east_text_detection.pb')
YOLO_DIR = Path(ANALYSIS_DIR, 'yolo_files')
BLOG_ROOT_URL = "blog"
AWS_S3_PHOTOS_DIR = "https://paris1970-fa22-dev-assets.s3.amazonaws.com/photos"

# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


ALLOWED_HOSTS = []  # For production, add domains

# Application definition

INSTALLED_APPS = [
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # 3rd party
    'rest_framework',
    'corsheaders',
    'webpack_loader',
    'django_extensions',
    'taggit',
    # wysiwyg for blog
    'tinymce',

    # our main application code
    'app',

    # our blog
    'blog',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BACKEND_DIR, 'templates'),
        ],
        'APP_DIRS': True,  # our app doesn't, but our third party apps do!
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'

LOGOUT_REDIRECT_URL = '/'

LOGIN_REDIRECT_URL = '/admin'

# DATABASES live in production and dev settings

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# the url where we'll look for static files
STATIC_URL = '/static/'

# the url where images will be uploaded

# where collectstatic puts static files for production
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')

# where collectstatic looks for static files
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'build'),
    os.path.join(PROJECT_ROOT, 'assets'),
)

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

}

CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
    'http://localhost:8000',
    'http://localhost:8080',
]

# Django webpack loader settings
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': './assets/bundles/',
        'STATS_FILE': os.path.join(PROJECT_ROOT, 'webpack-stats.json'),
    }
}

DEBUG = True

TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'silver',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
}
