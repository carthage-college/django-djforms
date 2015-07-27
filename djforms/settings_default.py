# -*- coding: utf-8 -*-
import os.path

#DEBUG = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('larry@carthage.edu'),
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
ROOT_URLCONF = 'djforms.core.urls'
MEDIA_ROOT = '/data2/django_projects/djforms/assets'
MEDIA_URL = '/assets/'
ROOT_DIR = os.path.dirname(__file__)
ROOT_URL = "/forms/"
STATIC_URL = '/djmedia/'
SERVER_URL = "www.carthage.edu"
API_URL = "%s/%s" % (SERVER_URL, "api")
API_KEY = ""
API_PEOPLE_URL=""
AUTH_PROFILE_MODULE = 'core.UserProfile'
SECRET_KEY = ''
HONEYPOT_FIELD_NAME=""
HONEYPOT_VALUE=""
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.word_challenge'
#CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
CAPTCHA_NOISE_FUNCTIONS = ''
CAPTCHA_DICTIONARY_MAX_LENGTH = 9
CAPTCHA_WORDS_DICTIONARY = '/d2/django_projects/djtools/fields/words.txt'
# Character Quest Window
CHARACTER_QUEST_END_MONTH = 4
CHARACTER_QUEST_END_DAY = 3
CHARACTER_QUEST_START_MONTH = 3
CHARACTER_QUEST_START_DAY = 1
# Celebration of Scholars Window
COS_END_MONTH = 3
COS_END_DAY = 23
COS_START_MONTH = 2
COS_START_DAY = 2
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
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
TEMPLATE_DIRS = (
    "/data2/django_projects/djforms/templates/",
    "/data2/django_templates/djdfir/",
    "/data2/django_templates/djcher/",

)
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
    'django.contrib.formtools',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.sites',

    # third party projects
    'authority',
    'bootstrapform',
    'captcha',
    'django_countries',
    'honeypot',
    'imagekit',
    #'oembed',
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
    'djforms.languages',
    'djforms.maintenance',
    'djforms.music.ensembles.choral',
    'djforms.music.theatre.summer_camp',
    'djforms.polisci.wipcs.proposal',
    'djforms.polisci.wipcs.registration',
    'djforms.president.honorary_degree',
    'djforms.processors',
    'djforms.scholars',
    'djforms.security',
    'djforms.sustainability.green',
    'djforms.writingcurriculum',
    'djtools'
)
# LDAP Constants
LDAP_SERVER = ''
LDAP_PORT = '636'
LDAP_PROTOCOL = "ldaps"
LDAP_BASE = ""
LDAP_USER = ""
LDAP_PASS = ""
LDAP_EMAIL_DOMAIN = ""
LDAP_OBJECT_CLASS = ""
LDAP_OBJECT_CLASS = ""
LDAP_OBJECT_CLASS_LIST = []
LDAP_GROUPS = {}
LDAP_RETURN = []
LDAP_ID_ATTR=""
# auth backends
AUTHENTICATION_BACKENDS = (
    'djauth.ldapBackend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
LOGIN_URL = '/forms/accounts/login/'
LOGOUT_URL = '/forms/accounts/logout/'
LOGIN_REDIRECT_URL = '/forms/'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# logggin stuff
LOG_FILEPATH = os.path.join(os.path.dirname(__file__), "logs/")
LOG_FILENAME = LOG_FILEPATH + "debug.log"
# SMTP settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_FAIL_SILENTLY = True
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
SERVER_MAIL=""
# email addresses
MAINTENANCE_MANAGER = ""
COS_DEFAULT_NAME = ""
COS_DEFAULT_EMAIL = ""
ALUMNI_OFFICE_EMAIL = ""
GIVING_DONATIONS_BCC = []
HONORARY_DEGREE_NOMINATION_EMAIL = ""
COMMUNICATIONS_METAMORPHOSIS_TO_LIST = []
# TLE applications
MODERN_LANGUAGES_TLE_APPLICATIONS = []
BIOLOGY_GENOMICS = []
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
TC_LIVE = False
TC_AVS = 'n'
#TC_AUTH_TYPE = "store"
TC_AUTH_TYPE = "sale"
TC_CYCLE = "1m"
TC_OPERATOR = "DJForms"
