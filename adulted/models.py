from django.db import models

from djforms.core.models import GENDER_CHOICES, BINARY_CHOICES
from djforms.processors.models import Contact

class Admissions(models.Model):
    contact = models.ForeignKey(Contact)
    dob     = models.DateField("Birthday", null=True, blank=True)
    gender  = models.CharField(max_length="16", choices=GENDER_CHOICES, null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.contact.fist_name, self.contact.last_name)

class School(object):

    def __init__(self, code, name, city, state, from_m, from_y, to_m, to_y, grad_m, grad_y):
        self.school_code    = code
        self.school_name    = name
        self.school_city    = city
        self.school_state   = state
        self.from_month     = from_m
        self.from_year      = from_y
        self.to_month       = to_m
        self.to_year        = to_y

