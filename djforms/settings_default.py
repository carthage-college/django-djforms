# -*- coding: utf-8 -*-
import os.path

from djzbar.settings import INFORMIX_EARL as INFORMIX_EARL

DEBUG = False
#DEBUG = True
TEMPLATE_DEBUG = DEBUG
INFORMIX_DEBUG = ""

ADMINS = (
    ('', ''),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'HOST': 'localhost',
        'NAME': '',
        'ENGINE': 'django.db.backends.mysql',
        'USER': '',
        'PASSWORD': '',
        'OPTIONS': {
           "init_command": "SET storage_engine=MyISAM",
        }
    },
}
ALLOWED_HOSTS =  ['localhost','127.0.0.1']
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
ROOT_URLCONF = 'djforms.core.urls'
MEDIA_ROOT = ''
MEDIA_URL = ''
ROOT_DIR = os.path.dirname(__file__)
UPLOADS_DIR = "files"
STATIC_URL = "/djmedia/"
ROOT_URL = "/forms/"
SERVER_URL = ""
API_URL = "%s/%s" % (SERVER_URL, "api")
LIVEWHALE_API_URL = "https://%s" % (SERVER_URL)
API_KEY = ""
API_PEOPLE_URL=""
AUTH_PROFILE_MODULE = 'core.UserProfile'
SECRET_KEY = ''
HONEYPOT_FIELD_NAME=""
HONEYPOT_VALUE=""
# Character Quest Window
CHARACTER_QUEST_END_MONTH = 4
CHARACTER_QUEST_END_DAY = 12
CHARACTER_QUEST_START_MONTH = 3
CHARACTER_QUEST_START_DAY = 1
# Celebration of Scholars Window
COS_END_MONTH = 4
COS_END_DAY = 30
COS_START_MONTH = 2
COS_START_DAY = 2
MIDDLEWARE_CLASSES = (
    #'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'honeypot.middleware.HoneypotMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
TEMPLATE_DIRS = ()
TEMPLATE_CONTEXT_PROCESSORS = (
    "djtools.context_processors.sitevars",
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
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',
    # third party projects
    'authority',
    'bootstrapform',
    'django_countries',
    'honeypot',
    'imagekit',
    'tagging',
    'userprofile',
    # djforms stuff
    'djforms.admissions',
    'djforms.admissions.admitted',
    'djforms.admissions.visitdays',
    'djforms.alumni.classnotes',
    'djforms.alumni.memory',
    'djforms.athletics.soccer',
    'djforms.biology.genomics',
    'djforms.catering',
    'djforms.characterquest',
    'djforms.communications.metamorphosis',
    'djforms.communications.printrequest',
    'djforms.core',
    'djforms.giving',
    'djforms.global_bridge',
    'djforms.jobpost',
    'djforms.lis',
    'djforms.lis.copyprint',
    'djforms.languages',
    'djforms.maintenance',
    'djforms.music.ensembles.choral',
    'djforms.music.theatre.summer_camp',
    'djforms.polisci.iea.proposal',
    'djforms.president.honorary_degree',
    'djforms.processors',
    'djforms.scholars',
    'djforms.security',
    'djforms.sustainability.green',
    'djforms.writingcurriculum',
    # other inhouse django apps
    'djtools',
)
# django-countries settings
COUNTRIES_FIRST = {
    'CN': ('China'),
    'US': ('United States'),
}
COUNTRIES_FLAG_URL = '/static/forms/img/flags/{code}.gif'
# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = ''
LDAP_PROTOCOL = ""
LDAP_BASE = ""
LDAP_USER = ""
LDAP_PASS = ""
LDAP_EMAIL_DOMAIN = ""
LDAP_OBJECT_CLASS = ""
LDAP_OBJECT_CLASS_LIST = []
LDAP_GROUPS = {}
LDAP_RETURN = []
LDAP_ID_ATTR=""
LDAP_AUTH_USER_PK = False
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.ldapBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '{}accounts/login/'.format(ROOT_URL)
LOGOUT_URL = '{}accounts/logout/'.format(ROOT_URL)
LOGIN_REDIRECT_URL = ROOT_URL
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_DOMAIN=""
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_NAME =''
SESSION_COOKIE_AGE = 86400
# CoS chapuza
COS_FACULTY = [{}]
# logggin stuff
LOG_FILEPATH = os.path.join(os.path.dirname(__file__), "logs/")
LOG_FILENAME = LOG_FILEPATH + "debug.log"
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%Y/%b/%d %H:%M:%S"
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt' : "%Y/%b/%d %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILENAME,
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'include_html': True,
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'djforms': {
            'handlers':['logfile'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
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
    }
}
# SMTP settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FAIL_SILENTLY = False
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL=""
# email addresses
SOCCER_CAMP_TO_LIST = []
MAINTENANCE_MANAGER = ""
COPYPRINT_CARD_REQUEST_EMAIL = ""
COS_DEFAULT_NAME = ""
COS_DEFAULT_EMAIL = ""
ALUMNI_OFFICE_EMAIL = ""
GIVING_DONATIONS_BCC = []
HONORARY_DEGREE_NOMINATION_EMAIL = ""
COMMUNICATIONS_METAMORPHOSIS_TO_LIST = []
CHARACTER_QUEST_TO_LIST = []
# TLE applications
MODERN_LANGUAGES_TLE_APPLICATIONS = []
BIOLOGY_GENOMICS = []
POLITICAL_SCIENCE_IEA_EMAIL = []
CONTINUING_STUDIES_ENRICHMENT_REGISTRATION_EMAIL = ""
ALUMNI_CLASSNOTES_EMAILS = []
CATERING_TO_LIST = []
# Authorize.net
GATEWAY_API_LOGIN = ""
GATEWAY_TRANS_KEY = ""
GATEWAY_USE_TEST_MODE = True
GATEWAY_USE_TEST_URL = True
GATEWAY_AUTHORIZE_ONLY = True
GATEWAY_NAME = "AimGateway"
# TrustCommerce
TC_LOGIN = ""
TC_PASSWORD = ""
#TC_LIVE = True
TC_LIVE = False
TC_AVS = 'n'
#TC_AUTH_TYPE = "store" # recurring subsciption
TC_AUTH_TYPE = "sale"
TC_CYCLE = "1m"
TC_OPERATOR = ""
