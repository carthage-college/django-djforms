from django.conf import settings

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = ["sdomin@carthage.edu","kjabeck@carthage.edu"]
BCC = settings.MANAGERS
