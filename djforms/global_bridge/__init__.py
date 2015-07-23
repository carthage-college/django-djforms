from django.conf import settings

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = [settings.SERVER_EMAIL,]
    #TO_LIST = ["tkline@carthage.edu",]
BCC = settings.MANAGERS
