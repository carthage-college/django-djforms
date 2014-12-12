"""
http://www.micahcarrick.com/authorize-net-credit-card-form-django.html
"""
from django.conf import settings

if settings.DEBUG:
    TO_LIST = [settings.SERVER_EMAIL,]
else:
    TO_LIST = ["sdomin@carthage.edu","kjabeck@carthage.edu"]
BCC = settings.MANAGERS
