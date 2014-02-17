from django.db import models

from djforms.core.models import GenericChoice
from djforms.processors.models import Contact
from tagging import fields, managers

class RegistrationContact(Contact):

    name_tag            = models.CharField("Name tag name", help_text="Name as you'd like it to appear on your name tag.", max_length="128", null=True, blank=True)
    affiliation         = models.CharField("Institution/Organization", max_length="256", null=True, blank=True)
    dietary_needs       = models.TextField(null=True, blank=True, help_text="Morning coffee, lunch, and snacks provided.")
    other_needs         = models.CharField(max_length="256", null=True, blank=True)

