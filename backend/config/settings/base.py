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
LOCAL_SRCS_DIR = Path(PROJECT_ROOT, 'assets', 'images', 'photos')
TEST_PHOTOS_DIR = Path(PROJECT_ROOT, 'backend', 'data', 'test_photos')
TESSDATA_DIR = Path(PROJECT_ROOT, 'backend', 'data', 'tessdata')
TEXT_DETECTION_PATH = Path(BACKEND_DATA_DIR, 'frozen_east_text_detection.pb')
YOLO_DIR = Path(ANALYSIS_DIR, 'yolo_files')

# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/


ALLOWED_HOSTS = []  # For production, add domains

# Application definition

INSTALLED_APPS = [
    'djangocms_admin_style',
    # django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd party
    'rest_framework',
    'corsheaders',
    'webpack_loader',
    'django_extensions',

    # our application code
    'app',
    'blog_app',

    # cms
    'cms',
    'menus',
    'treebeard',
    'sekizai',
    'filer',
    'easy_thumbnails',
    'mptt',
    'djangocms_text_ckeditor',
    'aldryn_apphooks_config',
    'parler',
    'taggit',
    'taggit_autosuggest',
    'meta',
    'sortedm2m',
    'djangocms_blog',

    # djangocms-bootstrap5
    'djangocms_icon',
    'djangocms_link',
    'djangocms_picture',
    'djangocms_bootstrap5',
    # 'djangocms_bootstrap5.contrib.bootstrap5_alerts',
    # 'djangocms_bootstrap5.contrib.bootstrap5_badge',
    # 'djangocms_bootstrap5.contrib.bootstrap5_card',
    # 'djangocms_bootstrap5.contrib.bootstrap5_carousel',
    # 'djangocms_bootstrap5.contrib.bootstrap5_collapse',
    # 'djangocms_bootstrap5.contrib.bootstrap5_content',
    # 'djangocms_bootstrap5.contrib.bootstrap5_grid',
    # 'djangocms_bootstrap5.contrib.bootstrap5_jumbotron',
    # 'djangocms_bootstrap5.contrib.bootstrap5_link',
    # 'djangocms_bootstrap5.contrib.bootstrap5_listgroup',
    # 'djangocms_bootstrap5.contrib.bootstrap5_media',
    # 'djangocms_bootstrap5.contrib.bootstrap5_picture',
    # 'djangocms_bootstrap5.contrib.bootstrap5_tabs',
    # 'djangocms_bootstrap5.contrib.bootstrap5_utilities',
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
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # cms
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
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

                # cms
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
                'django.template.context_processors.i18n'
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BACKEND_DIR, 'db.sqlite3'),
    }
}

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

# the url where we'll look for media files
MEDIA_URL = "/media/"

# where uploaded files are stored
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")

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

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

META_SITE_PROTOCOL = 'http'  # set 'http' for non ssl enabled websites

META_USE_OG_PROPERTIES = True
META_USE_TWITTER_PROPERTIES = True
META_USE_GOOGLEPLUS_PROPERTIES = True  # django-meta 1.x+
META_USE_SCHEMAORG_PROPERTIES = True  # django-meta 2.x+

META_USE_SITES = True

DEBUG = True
