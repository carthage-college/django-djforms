from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.localflavor.us.models import USStateField

from djforms.core.models import GenericContact

class Attendee(GenericContact):
    maiden_name     = models.CharField(max_length=128, null=True, blank=True)
    # dates
    created_on      = models.DateTimeField("Date Created", auto_now_add=True)
    updated_on      = models.DateTimeField("Date Updated", auto_now=True)
    #core
    grad_class      = models.CharField("Graduating class", max_length=4)
    city            = models.CharField(max_length=128, null=True, blank=True)
    state           = USStateField(null=True, blank=True)
    guests          = models.CharField("Number of guests", max_length=2)

    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)

