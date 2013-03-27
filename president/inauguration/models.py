from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.localflavor.us.models import USStateField

from djforms.core.models import GenericContact, BINARY_CHOICES

class RsvpContact(GenericContact):
    institution     = models.CharField("Name of Institution", max_length=128)
    year_founded    = models.CharField("Year Founded",max_length=4)
    job_title       = models.CharField("Delegate's Title", max_length=128)
    cohort          = models.CharField("Guest's name", max_length=128)
    address         = models.CharField(max_length=256)
    city            = models.CharField(max_length=128)
    state           = USStateField()
    postal_code     = models.CharField(max_length=10, verbose_name = 'Zip code')
    phone           = models.CharField("Telephone", max_length=12, help_text="Format: XXX-XXX-XXXX")
    march           = models.CharField("Delegate will march in the academic procession", max_length=3, choices=BINARY_CHOICES)
    attend          = models.CharField("I will attend the Inaugural Luncheon", max_length=3, choices=BINARY_CHOICES)
    guest_attend    = models.CharField("My guest will also attend this event", max_length=3, choices=BINARY_CHOICES)

    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)
