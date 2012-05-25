from django.db import models

from djforms.core.models import GENDER_CHOICES, BINARY_CHOICES
from djforms.processors.models import Contact

class Admissions(models.Model):
    contact = models.ForeignKey(Contact)
    dob     = models.DateField("Birthday", null=True, blank=True)
    gender  = models.CharField(max_length="16", choices=GENDER_CHOICES, null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.contact.fist_name, self.contact.last_name)

