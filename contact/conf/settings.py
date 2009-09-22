# -*- coding: utf-8 -*-

from django.conf import settings

DEBUG = getattr(settings, 'DEBUG', True)
MAIL_ADMINS = getattr(settings, 'CONTACT_MAIL_ADMINS', False)
MAIL_MANAGERS = getattr(settings, 'CONTACT_MAIL_MANAGERS', True)
USE_FORM_EMAIL = getattr(settings, 'CONTACT_USE_FORM_EMAIL', False)
FROM_EMAIL = getattr(settings,
                     'CONTACT_FROM_EMAIL',
                     'webmaster@carthage.edu')
NOTIFY_SENT = getattr(settings, 'CONTACT_NOTIFY_SENT', True)
FAIL_SILENTLY = getattr(settings, 'CONTACT_FAIL_SILENTLY', True)
DEFAULT_TEMPLATE = 'contact/message.txt'
