from django.conf import settings

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = settings.POLITICAL_SCIENCE_IEA_EMAIL
BCC = settings.MANAGERS
