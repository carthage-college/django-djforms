from django.db import models

from djforms.processors.models import Contact


class Registration(Contact):

    affiliation = models.CharField(
        "Institution/Organization", max_length="256", null=True, blank=True
    )
    job_title = models.CharField(
        max_length="128", null=True, blank=True
    )

    class Meta:
        db_table = 'course_ference_attender'
