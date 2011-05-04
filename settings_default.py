# -*- coding: utf-8 -*-
import os.path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    (''),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'HOST': 'localhost',
        'NAME': 'djforms',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': ''
    },
}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
ROOT_URLCONF = 'djforms.urls'
MEDIA_ROOT = '/data2/django_projects/djforms/assets'
MEDIA_URL = '/assets/'
ADMIN_MEDIA_PREFIX = '/djmedia/'
AUTH_PROFILE_MODULE = 'core.UserProfile'
SECRET_KEY = ''

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = (
    "/data2/django_projects/djforms/templates/",
    "/data2/django_projects/sputnik/production/sputnik/templates/"
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "djforms.context_processors.sitevars",
    #"django.core.context_processors.auth",
    "django.contrib.auth.context_processors.auth",
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
    'oembed',
    'tagging',
    'userprofile',
    # djforms stuff
    'djforms.admissions',
    'djforms.admissions.visitdays',
    'djforms.alumni',
    'djforms.alumni.memory',
    'djforms.alumni.msw',
    'djforms.characterquest',
    'djforms.core',
    'djforms.jobpost',
    'djforms.languages',
    'djforms.maintenance',
    'djforms.lacrossegolfinvite',
    'djforms.security',
    'djforms.video',
    'djforms.writingcurriculum',
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
#EMAIL_USE_TLS = True
#EMAIL_HOST = 'smtp.gmail.com'
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL=""
