from django.conf import settings

REG_FEE = 40000
if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = ["tkline@carthage.edu",]
BCC = settings.MANAGERS
