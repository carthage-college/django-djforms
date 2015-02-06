from django.conf import settings

REG_FEE = 2800
if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = ["cness@carthage.edu","kflister@carthage.edu"]
BCC = settings.MANAGERS
