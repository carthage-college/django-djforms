# -*- coding: utf-8 -*-

"""Django settings for project."""

import os

# Debug
DEBUG = False
INFORMIX_DEBUG = ''
REQUIRED_ATTRIBUTE = True
ADMINS = ()
MANAGERS = ADMINS
SECRET_KEY = None
ENCRYPTION_KEY = None
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Chicago'
TIME_INPUT_FORMATS = ('%H:%M %p',)
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = False
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
SERVER_URL = ''
API_URL = '{0}/{1}'.format(SERVER_URL, 'api')
API_KEY = ''
API_PEOPLE_URL = ''
LIVEWHALE_API_URL = 'https://{0}'.format(SERVER_URL)
ROOT_URLCONF = 'djforms.core.urls'
WSGI_APPLICATION = 'djforms.wsgi.application'
AUTH_PROFILE_MODULE = 'core.UserProfile'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = BASE_DIR
PROJECT_APP = os.path.basename(BASE_DIR)
ROOT_URL = '/forms/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
UPLOADS_DIR = 'files'
MEDIA_ROOT = '{0}/assets/'.format(ROOT_DIR)
STATIC_ROOT = '{0}/static/'.format(ROOT_DIR)
STATIC_URL = '/static/{0}/'.format(PROJECT_APP)
MEDIA_URL = '/media/{0}/'.format(PROJECT_APP)
X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs4'
FILE_UPLOAD_PERMISSIONS = 0o644
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
DATABASES = {
    'default': {
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'NAME': 'django_djforms',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': '',
    },
}
INSTALLED_APPS = (
    # django apps
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    # third party projects
    'bootstrapform',
    'django_countries',
    'django_summernote',
    'captcha',
    'honeypot',
    'imagekit',
    'loginas',
    'taggit',
    # djforms stuff
    'djforms.admissions',
    'djforms.admissions.admitted',
    'djforms.admissions.visitdays',
    'djforms.alumni.classnotes',
    'djforms.alumni.memory',
    'djforms.athletics.soccer',
    'djforms.communications.printrequest',
    'djforms.core',
    'djforms.giving',
    'djforms.lis',
    'djforms.lis.copyprint',
    'djforms.languages',
    'djforms.music.ensembles.choral',
    'djforms.prehealth.committee_letter',
    'djforms.processors',
    'djforms.scholars',
    'djforms.security',
    'djforms.writingcurriculum',
    # other in-house django apps
    'djtools',
)
MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
# template stuff
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            '/data2/django_templates/djkali/',
            '/data2/django_templates/djcher/',
            '/data2/django_templates/',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'djtools.context_processors.sitevars',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# caching
#CACHES = {
    #'default': {
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'LOCATION': '127.0.0.1:11211',
        #'TIMEOUT': 60*60*24,
        #'KEY_PREFIX': '{0}_'.format(PROJECT_APP),
    #}
#}
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = ''
LDAP_PROTOCOL = ''
LDAP_BASE = ''
LDAP_USER = ''
LDAP_PASS = None
LDAP_OBJECT_CLASS = ''
LDAP_GROUPS = None
LDAP_RETURN = ()
LDAP_ID_ATTR = ''
LDAP_AUTH_USER_PK = False
LDAP_EMAIL_DOMAIN = ''
LDAP_OBJECT_CLASS_LIST = []
LDAP_GROUPS = {}
LDAP_RETURN = []
LDAP_ID_ATTR = ''
LDAP_AUTH_USER_PK = False
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.backends.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '{0}accounts/login/'.format(ROOT_URL)
LOGOUT_URL = '{0}accounts/logout/'.format(ROOT_URL)
LOGIN_REDIRECT_URL = ROOT_URL
USE_X_FORWARDED_HOST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_DOMAIN='.carthage.edu'
SESSION_COOKIE_NAME = 'django_djforms_cookie'
SESSION_COOKIE_AGE = 86400
# security
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True
# SMTP settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FAIL_SILENTLY = True
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL = ''
# logging
LOG_FILEPATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs/',
)
LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
DEBUG_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'debug.log')
INFO_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'info.log')
ERROR_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'error.log')
CUSTOM_LOG_FILENAME = '{0}{1}'.format(LOG_FILEPATH, 'custom.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': '%Y/%b/%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILENAME,
            'formatter': 'standard',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'include_html': True,
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'custom_logfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': CUSTOM_LOG_FILENAME,
            'formatter': 'custom',
        },
        'info_logfile': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 10,
            'maxBytes': 50000,
            'filename': INFO_LOG_FILENAME,
            'formatter': 'simple',
        },
        'debug_logfile': {
            'level': 'DEBUG',
            'handlers': ['logfile'],
            'class': 'logging.FileHandler',
            'filename': DEBUG_LOG_FILENAME,
            'formatter': 'verbose',
        },
        'error_logfile': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': ERROR_LOG_FILENAME,
            'formatter': 'verbose',
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
# Soccer camp
SOCCER_CAMP_MONTH=9
SOCCER_CAMP_DAY=1
# django-countries
COUNTRIES_FIRST = {
    'US': ('United States'),
}
COUNTRIES_FLAG_URL = '/static/forms/img/flags/{code}.gif'
# Celebration of Scholars Window
COS_END_MONTH = 5
COS_END_DAY = 1
COS_START_MONTH = 2
COS_START_DAY = 2
COS_EMAIL = ''
COS_FACULTY = [{}]
# giving constants
GIVING_DEFAULT_CONTACT_FORM = ''
GIVING_DEFAULT_CAMPAIGN = 'default'
GIVING_DAY_START_DATE = ''
GIVING_DAY_END_DATE = ''
GIVING_DAY_CAPTION_FILE = ''
GIVING_DAY_CAPTION_FILE_ORIG = '{0}/{1}/giving/{2}'.format(
    MEDIA_ROOT, UPLOADS_DIR, GIVING_DAY_CAPTION_FILE,
)
GIVING_DAY_CAPTION_FILE_NEW = '{0}/{1}/giving/new_{2}'.format(
    MEDIA_ROOT, UPLOADS_DIR, GIVING_DAY_CAPTION_FILE,
)
GIVING_DAY_FONT = '/d2/www/static/forms/fonts/PermanentMarker.ttf'
# email addresses
SOCCER_CAMP_TO_LIST = []
INSURANCE_TO_LIST = []
COPYPRINT_CARD_REQUEST_EMAIL = ''
COS_DEFAULT_NAME = ''
COS_DEFAULT_EMAIL = ''
ALUMNI_OFFICE_EMAIL = ''
ALUMNI_MEMORY_EMAIL = []
GIVING_DONATIONS_BCC = []
HONORARY_DEGREE_NOMINATION_EMAIL = ''
COMMUNICATIONS_METAMORPHOSIS_TO_LIST = []
COMMUNICATIONS_PRINT_REQUEST_EMAIL = ''
ADMISSIONS_ADMITTED_EMAIL_LIST = []
ADMISSIONS_EMAIL = ''
ADMISSIONS_BCC = []
POLISCI_MODEL_UN_TO_LIST = []
# TLE applications
MODERN_LANGUAGES_TLE_APPLICATIONS = []
STUDY_ABROAD_EMAIL = ''
ALUMNI_CLASSNOTES_EMAILS = []
LIS_PRINT_REQUEST_EMAIL = ''
CHORAL_TRYOUTS_FROM = ''
PREHEALTH_CC = ''
PREHEALTH_DO = ''
PREHEALTH_MD = ''
WAC_EMAIL_LIST = []
SECURITY_PARKING_TICKET_APPEAL_EMAIL = ''
SECURITY_REPORT_EMAIL = ''
# Authorize.net
GATEWAY_API_LOGIN = ''
GATEWAY_TRANS_KEY = ''
GATEWAY_USE_TEST_MODE = True
GATEWAY_USE_TEST_URL = True
GATEWAY_AUTHORIZE_ONLY = True
GATEWAY_NAME = 'AimGateway'
# TrustCommerce
TC_LOGIN = ''
TC_PASSWORD = ''
TC_LIVE = True
TC_AVS = 'n'
#TC_AUTH_TYPE = 'store' # recurring subsciption
TC_AUTH_TYPE = 'sale'
TC_CYCLE = '1m'
TC_OPERATOR = 'DJForms'
# simple captcha
CAPTCHA_BACKGROUND_COLOR='#ffffff'
CAPTCHA_FOREGROUND_COLOR='#000000'
CAPTCHA_NOISE_FUNCTIONS=('captcha.helpers.noise_null',)
#CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
# recaptcha
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
# in use?
NOCAPTCHA = True

##################
# LOCAL SETTINGS #
##################

# Allow any settings to be defined in local.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.

# Instead of doing "from .local import *", we use exec so that
# local has full access to everything defined in this module.
# Also force into sys.modules so it's visible to Django's autoreload.

phile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'local.py')
if os.path.exists(phile):
    import imp
    import sys
    module_name = '{0}.settings.local'.format(PROJECT_APP)
    module = imp.new_module(module_name)
    module.__file__ = phile
    sys.modules[module_name] = module
    exec(open(phile, 'rb').read())
