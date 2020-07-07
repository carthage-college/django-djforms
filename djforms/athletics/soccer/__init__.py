from django.conf import settings

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL]
    INSURANCE_TO_LIST = [settings.SERVER_EMAIL]
else:
    TO_LIST = settings.SOCCER_CAMP_TO_LIST
    INSURANCE_TO_LIST = settings.INSURANCE_TO_LIST
BCC = settings.MANAGERS
