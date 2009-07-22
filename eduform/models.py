from django.db import models
from django.forms import ModelForm
from djforms.core.models import GenericContact, GenericChoice

from django.contrib.auth.models import User

from tagging.fields import TagField
from tagging.models import Tag

TIME_CHOICES=[  ('Morning', 'Morning'),
                ('Afternoon', 'Afternoon'),
                ('Evening', 'Evening')]

class EduProfile(GenericContact):
    phone = models.CharField(max_length=30, verbose_name='Phone Number')
    address = models.TextField(verbose_name='mailing Address')
    contact_time = models.CharField(max_length=1, choices=TIME_CHOICES, verbose_name='Best time to contact you')
    programs_of_interest = models.ManyToManyField(GenericChoice, related_name="edu_profile_programs_of_interest") 
    hear_about_us = models.TextField(blank=True, verbose_name='How did you hear about us?')
