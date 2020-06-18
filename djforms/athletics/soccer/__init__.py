from django.conf import settings

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL]
    INSURANCE_TO_LIST = ['sdomin@carthage.edu', settings.SERVER_EMAIL]
else:
    TO_LIST = settings.SOCCER_CAMP_TO_LIST
    INSURANCE_TO_LIST = settings.SOCCER_CAMP_TO_LIST
    INSURANCE_TO_LIST.append('soccercamprecords@carthage.edu')
BCC = settings.MANAGERS
