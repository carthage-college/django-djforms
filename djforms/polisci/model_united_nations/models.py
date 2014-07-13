from django.db import models
from djforms.processors.models import Contact

class Attender(Contact):
    """
    Model United Nations attender contact
    """
    school_name = models.CharField(
        "School name",
        max_length=100
    )
    office = models.CharField(max_length=100)
    #home_phone = models.CharField(
    #    "Home phone",
    #    max_length=12,
    #    null=True, blank=True
    #)
    number_of_del = models.CharField(
        "Number of delegations"
    )
    number_of_stu = models.CharField(
        "Number of students",
        max_length=3
    )
    comments = models.CharField(
        "Questions/Comments",
        null=True, blank=True
    )

class Countries(models.Model):
    name = models.CharField(
        "Country name",
        max_length=128
    )
    status = models.BooleanField(default=True)

