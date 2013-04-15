from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.localflavor.us.models import USStateField

from djforms.core.models import GenericContact, BINARY_CHOICES

class RsvpContact(GenericContact):
    institution     = models.CharField("Name of institution", max_length=128)
    year_founded    = models.CharField("Year founded", max_length=4, null=True, blank=True)
    job_title       = models.CharField("Delegate's title", max_length=128)
    degree          = models.CharField("Delegate's highest degree", max_length=128)
    cohort          = models.CharField("Guest's name", max_length=128)
    address1        = models.CharField("Delegate's Preferred Mailing Address", max_length=256)
    address2        = models.CharField("", max_length=256, null=True, blank=True)
    city            = models.CharField(max_length=128)
    state           = USStateField()
    postal_code     = models.CharField(max_length=10, verbose_name = 'Zip code')
    phone           = models.CharField("Telephone", max_length=12, help_text="Format: XXX-XXX-XXXX")
    march           = models.CharField("Delegate will march in the academic procession", max_length=3, choices=BINARY_CHOICES)
    attend          = models.CharField("I will attend the Inaugural Luncheon", max_length=3, choices=BINARY_CHOICES)
    guest_attend    = models.CharField("My guest will also attend this event", max_length=3, choices=BINARY_CHOICES)

    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)
