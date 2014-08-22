from django.conf import settings

if settings.DEBUG:
    TO_LIST = ["larry@carthage.edu",]
else:
    TO_LIST = ["darion@carthage.edu",]
BCC = settings.MANAGERS

