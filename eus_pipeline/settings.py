"""
Django settings for eus_pipeline project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True
ALLOWED_HOSTS = []
try:
    # settings_local should define SECRET_KEY, DEBUG, and ALLOWED_HOSTS
    from settings_local import *
except ImportError:
    pass
TEMPLATE_DEBUG = DEBUG


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'blurbs',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'eus_pipeline.urls'

WSGI_APPLICATION = 'eus_pipeline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'blurbs.db'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Montreal'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'eus_pipeline', 'media')

MEDIA_URL = 'http://localhost:8000/media/'

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'eus_pipeline', 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'eus_pipeline', 'templates'),
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

TINYMCE_JS_URL = '//cdn.jsdelivr.net/tinymce/3.5.8/tiny_mce.js'
TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'plugins': 'paste',
    'theme_advanced_statusbar_location': 'none',
    'theme_advanced_toolbar_location': 'bottom',
    'theme_advanced_buttons1': ''.join((
        'bold,italic,underline,strikethrough,separator,',
        'undo,redo,separator,bullist,numlist,separator,link,unlink,',
        'separator,removeformat')),
    'theme_advanced_buttons2': '',
    'theme_advanced_buttons3': '',
    'theme_advanced_toolbar_align': 'center',
    'paste_text_sticky': True,
    'paste_text_sticky_default': True,
    'invalid_elements': 'pre,div',
}
