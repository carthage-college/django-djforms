from django.db import models

from djforms.core.models import GenericChoice
from djforms.processors.models import Contact
from tagging import fields, managers

class CourseFerenceRegistration(Contact):

    affiliation         = models.CharField("Institution/Organization", max_length="256", null=True, blank=True)
    job_title           = models.CharField(max_length="128", null=True, blank=True)

    class Meta:
        db_table = 'course_ference_registration'
