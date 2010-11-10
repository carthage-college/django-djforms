from django.db import models
from django.contrib.localflavor.us.models import USStateField

from djforms.core.models import GenericContact, GENDER_CHOICES, YEAR_CHOICES

from tagging.fields import TagField

class VisitDayEvent(models.Model):
    date            = models.DateField()
    start           = models.TimeField("Starts at", null = True, blank = True, help_text="(format HH:MM am/pm)")
    end             = models.TimeField("Ends at", null = True, blank = True, help_text="(format HH:MM am/pm)")
    max_attendees   = models.IntegerField()
    cur_attendees   = models.IntegerField()
    active          = models.BooleanField(default=True)
    tags            = TagField()

class VisitDayBaseProfile(GenericContact):
    date            = models.ForeignKey(VisitDayEvent)
    address         = models.CharField(max_length=255, verbose_name = 'Address')
    city            = models.CharField(max_length=128, verbose_name = 'City')
    state           = USStateField()
    zip             = models.CharField(max_length=10, verbose_name = 'Zip code')
    phone           = models.CharField(max_length=12, verbose_name='Phone Number', help_text="Format: XXX-XXX-XXXX")
    mobile          = models.CharField(max_length=12, verbose_name='Mobile Phone', help_text="Format: XXX-XXX-XXXX", null=True, blank=True)
    gender          = models.CharField(max_length="16", choices=GENDER_CHOICES)
    number_attend   = models.IntegerField()

class VisitDayProfile(VisitDayBaseProfile):
    high_school     = models.CharField()
    hs_city         = models.CharField()
    hs_state        = USStateField()
    hs_grad_year    = models.IntegerField()
    entry_as        = models.CharField("Entering as a", max_length="1", choices=YEAR_CHOICES)
    entry_year      = models.IntegerField()
    entry_term      = models.CharField()
    academic        = models.TextField("Academic Interests")
    xtracurricular  = models.TextField("Extracurricular Interests")
    comments        = models.TextField(null=True, blank=True)

