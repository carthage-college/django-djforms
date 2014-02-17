from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.localflavor.us.models import USStateField

from djforms.core.models import GenericContact

class ReunionContact(GenericContact):
    #core
    cohort          = models.CharField(max_length=128)
    address         = models.CharField(max_length=255)
    city            = models.CharField(max_length=128)
    state           = USStateField()
    postal_code     = models.CharField(max_length=10, verbose_name = 'Zip code')
    phone           = models.CharField('Telephone', max_length=12, help_text="Format: XXX-XXX-XXXX")
    employer        = models.CharField("Current Employer", max_length=100, null=True, blank=True)
    job_title       = models.CharField(max_length=100, null=True, blank=True)
    job_duties      = models.TextField('Duties', null=True, blank=True)
    licensure       = models.CharField(max_length=255, null=True, blank=True)
    achievements    = models.TextField('Professional Achievements', null=True, blank=True)
    memory          = models.TextField('Favorite Memory about your time at LUC/Carthage')
    update          = models.TextField('Brief Update', help_text="What's Happened Since You Graduated (500 characters max)")


    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return reverse("reunion_contact_detail", args=[self.pk])
