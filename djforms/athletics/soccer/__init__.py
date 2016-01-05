from django.conf import settings

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = settings.SOCCER_CAMP_TO_LIST
BCC = settings.MANAGERS
