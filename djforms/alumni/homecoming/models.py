from django.db import models

from djforms.core.models import GenericContact

from localflavor.us.models import USStateField

class Attendee(GenericContact):
    maiden_name = models.CharField(max_length=128, null=True, blank=True)
    #core
    grad_class = models.CharField("Graduating class", max_length=4)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = USStateField(null=True, blank=True)
    guests = models.CharField("Number of guests", max_length=2)

    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)

