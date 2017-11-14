# -*- coding: utf-8 -*-
import os.path

from datetime import datetime

DEBUG = False
DEBUG = True

ADMINS = (
    ('', ''),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'HOST': '',
        'PORT': '',
        'NAME': '',
        'ENGINE': '',
        'USER': '',
        'PASSWORD': '',
        'OPTIONS': {
           "init_command": "SET storage_engine=MyISAM",
        }
    },
}

ALLOWED_HOSTS =  []
TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'
ROOT_URLCONF = 'djforms.core.urls'
MEDIA_ROOT = '/data2/django_projects/djforms/assets/'
MEDIA_URL = '/static/forms/assets/'
UPLOADS_DIR = 'files'
ROOT_DIR = os.path.dirname(__file__)
STATIC_URL = '/djmedia/'
ROOT_URL = '/forms/'
SERVER_URL = ''
API_URL = '{}/{}'.format(SERVER_URL, 'api')
LIVEWHALE_API_URL = 'https://{}'.format(SERVER_URL)
API_KEY = ''
API_PEOPLE_URL = ''
AUTH_PROFILE_MODULE = 'core.UserProfile'
SECRET_KEY = ''
HONEYPOT_FIELD_NAME=''
HONEYPOT_VALUE=''

# Character Quest Window
CHARACTER_QUEST_END_MONTH = 5
CHARACTER_QUEST_END_DAY = 1
CHARACTER_QUEST_START_MONTH = 3
CHARACTER_QUEST_START_DAY = 1
# Celebration of Scholars Window
COS_END_MONTH = 3
COS_END_DAY = 31
COS_START_MONTH = 2
COS_START_DAY = 2
# giving constants
GIVING_DEFAULT_CONTACT_FORM = 'GivingDay'
GIVING_DEFAULT_CAMPAIGN = 'giving-day'
GIVING_DAY_START_DATE = datetime.strptime(
    'May 1 2018 4:20PM','%b %d %Y %I:%M%p'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'honeypot.middleware.HoneypotMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(os.path.dirname(__file__), 'templates'),
            "/data2/django_templates/djkorra/",
            "/data2/django_templates/djcher/",
            "/data2/django_templates/",
        ],
        'OPTIONS': {
            'debug':DEBUG,
            'context_processors': [
                "djtools.context_processors.sitevars",
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader'
            ]
        },
    },
]
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
    #'authority',
    'bootstrapform',
    'django_countries',
    'honeypot',
    'imagekit',
    #'oembed',
    'taggit',
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
    'djforms.languages',
    'djforms.lis.copyprint',
    'djforms.lis.conferences.mathematica',
    'djforms.music.ensembles.choral',
    'djforms.music.theatre.summer_camp',
    'djforms.polisci.iea.proposal',
    'djforms.polisci.iea.registration',
    'djforms.prehealth.committee_letter',
    'djforms.processors',
    'djforms.scholars',
    'djforms.security',
    'djforms.sustainability.green',
    'djforms.writingcurriculum',
    # other inhouse django
    'djtools',
)
COUNTRIES_FIRST = {
    'US': ('United States'),
}
COUNTRIES_FLAG_URL = '/static/forms/img/flags/{code}.gif'
# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = ''
LDAP_PROTOCOL = ''
LDAP_BASE = ''
LDAP_USER = ''
LDAP_PASS = ''
LDAP_EMAIL_DOMAIN = ''
LDAP_OBJECT_CLASS = ''
LDAP_OBJECT_CLASS_LIST = []
LDAP_GROUPS = {}
LDAP_RETURN = []
LDAP_ID_ATTR = ''
LDAP_AUTH_USER_PK = False
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.ldapBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = ''
LOGOUT_URL = ''
LOGIN_REDIRECT_URL = ''
USE_X_FORWARDED_HOST = True
SESSION_COOKIE_DOMAIN = ''
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_NAME = ''
SESSION_COOKIE_AGE = 86400
COS_FACULTY = [{ }]
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
EMAIL_FAIL_SILENTLY = True
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL = ''
# email addresses
SOCCER_CAMP_TO_LIST = []
MAINTENANCE_MANAGER = ''
CHARACTER_QUEST_TO_LIST = []
COPYPRINT_CARD_REQUEST_EMAIL = ''
COS_DEFAULT_NAME = ''
COS_DEFAULT_EMAIL = ''
ALUMNI_OFFICE_EMAIL = ''
GIVING_DONATIONS_BCC = []
COMMUNICATIONS_METAMORPHOSIS_TO_LIST = []
MODEL_UN_TO_LIST = []
# TLE applications
MODERN_LANGUAGES_TLE_APPLICATIONS = []
STUDY_ABROAD_EMAIL = ''
BIOLOGY_GENOMICS = []
POLITICAL_SCIENCE_IEA_EMAIL = []
CONTINUING_STUDIES_ENRICHMENT_REGISTRATION_EMAIL = ''
ALUMNI_CLASSNOTES_EMAILS = []
CATERING_TO_LIST = []
LIS_MATHEMATICA_REGISTRATION_EMAIL = []
CHORAL_TRYOUTS_FROM = ''
PREHEALTH_DO = ''

# Authorize.net
GATEWAY_API_LOGIN = ''
GATEWAY_TRANS_KEY = ''
GATEWAY_USE_TEST_MODE = True
GATEWAY_USE_TEST_URL = True
GATEWAY_AUTHORIZE_ONLY = True
GATEWAY_NAME = ''
# TrustCommerce
TC_LOGIN = ''
TC_PASSWORD = ''
TC_LIVE = False
TC_AVS = 'n'
#TC_AUTH_TYPE = 'store' # recurring subsciption
TC_AUTH_TYPE = 'sale'
TC_CYCLE = '1m'
TC_OPERATOR = ''
# caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #'LOCATION': '127.0.0.1:11211',
        #'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        #'LOCATION': '/var/tmp/django_directory_cache',
        #'TIMEOUT': 60*60*24*365,
        #'KEY_PREFIX': "DJFORMS_",
        #'OPTIONS': {
        #    'MAX_ENTRIES': 100000,
        #    'CULL_FREQUENCY': 4,
        #}
    }
}
