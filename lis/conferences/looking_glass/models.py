from django.db import models

from djforms.core.models import GenericChoice
from djforms.processors.models import Contact
from tagging import fields, managers

class RegistrationContact(Contact):

    name_tag            = models.CharField("Name tag name", help_text="Name as you'd like it to appear on your nametag.", max_length="128", null=True, blank=True)
    affiliation         = models.CharField(max_length="256", null=True, blank=True)
    dietary_needs       = models.TextField(null=True, blank=True)
    other_needs         = models.CharField(max_length="256", null=True, blank=True)
    housing             = models.BooleanField(default=False)
    event               = models.ManyToManyField(GenericChoice, verbose_name="Conference Events", related_name="conference_events")

