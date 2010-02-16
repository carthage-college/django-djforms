# -*- coding: utf-8 -*-
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('', ''),
)
MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = '!'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
DATABASE_NAME = 'djforms'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True

ROOT_URLCONF = 'djforms.urls'
MEDIA_ROOT = '/data2/django_projects/djforms/assets'
MEDIA_URL = '/assets/'
ADMIN_MEDIA_PREFIX = '/djmedia/'
AUTH_PROFILE_MODULE = 'core.UserProfile'
SECRET_KEY = 'zp(!1yvo=g1j58@)29m$bxpl5$o3-g5i!$z*##jbfz=j_(g&-)'
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
TEMPLATE_DIRS = (
    "/data2/django_projects/djforms/templates/",
    "/data2/django_projects/sputnik/production/sputnik/templates/"
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "djforms.context_processors.sitevars",
    "django.core.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    "django.core.context_processors.media",
)
INSTALLED_APPS = (
    # django apps
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    # third party projects
    'authority',
    'imagekit',
    'tagging',
    # djforms stuff
    'djforms.alumni',
    'djforms.alumni.memory',
    'djforms.core',
    #'djforms.eduform',
    #'djforms.forms',
    'djforms.jobpost',
    #'djforms.eventform',
    'djforms.maintenance',
)
# auth stuff
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    #'djforms.auth.ldapBackend.LDAPBackend',
)
LOGIN_URL = '/forms/accounts/login/'
LOGIN_REDIRECT_URL = '/forms/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# logggin stuff
LOG_FILEPATH = os.path.join(os.path.dirname(__file__), "logs/")
LOG_FILENAME = LOG_FILEPATH + "debug.log"
# SMTP settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'webmaster@carthage.edu'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
