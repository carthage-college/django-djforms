from django.conf import settings

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = ["dusinger@carthage.edu","jroberg@carthage.edu"]
BCC = settings.MANAGERS
