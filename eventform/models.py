from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from djforms.core.models import GenericContact, GenericChoice
from django.db.models import permalink
import datetime

EVENT_TYPE_CHOICES = (
    ('capture', 'Capture Carthage'),
    ('preview', 'Preview Days'),
    ('fallvisit', 'Fall Visit Days'),
    ('summervisit', 'Summer Visit Days'),
)

SEX_CHOICES = (
    ('f', 'Female'),
    ('m', 'Male'),
)

class Event(models.Model):
    title          = models.CharField(max_length=100, verbose_name = 'Event name')
    slug           = models.SlugField(unique=True)
    event_type     = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    event_date     = models.DateTimeField()
    capacity       = models.IntegerField(max_length=5, null=True, blank=True)
    contact_name   = models.CharField(max_length=100, verbose_name = 'Event Contact', null=True, blank=True)
    contact_phone  = models.CharField(max_length=100, verbose_name = 'Contact Phone', null=True, blank=True)
    contact_email  = models.CharField(max_length=100, verbose_name = 'Contact Email', null=True, blank=True)
    contact_office = models.CharField(max_length=100, verbose_name = 'Contact Email', null=True, blank=True)

    class Meta:
        ordering = ('title',)

    class Admin:
        prepopulated_fields = {'slug': ('title',)}

    def __unicode__(self):
        return '%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ('event_detail', None, {'slug':self.slug })

#uses the generic choice field from the core app
class AdmissionVisitRegistrant(GenericContact):
    event               = models.ForeignKey(Event)
    city                = models.CharField(max_length=255)
    state               = models.CharField(max_length=50)
    zip                 = models.CharField(max_length=12)
    phone               = models.CharField(max_length=255)
    registrant_id       = models.IntegerField(max_length=12, null=True, blank=True)
    number_attending    = models.IntegerField(max_length=3)
    sex                 = models.CharField(max_length=1, choices=SEX_CHOICES))
    high_school         = models.CharField(max_length=255)
    hs_city_state       = models.CharField(max_length=255)
    hs_grad_year        = models.ForeignKey(GenericChoice, related_name="event_grad_year")
    entering_as         = models.ForeignKey(GenericChoice, related_name="event_entering_as")
    entry_year          = models.ForeignKey(GenericChoice, related_name="event_entry_year")
    entry_term          = models.ForeignKey(GenericChoice, related_name="event_entry_term")
    academic            = models.TextField('Academic Interests')
    extracurricular     = models.TextField('Extracurricular Interests')
    submitted_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering  = ('-submitted_at',)

    def __unicode__(self):
        return u'%s %s' % (first_name, last_name)

