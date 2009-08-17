from django.db import models
from django.forms import ModelForm

from django.contrib.auth.models import User
from tagging.fields import TagField
from tagging.models import Tag

import datetime

#For making choices for choice fields for forms
class GenericChoice(models.Model):
    name = models.CharField(unique=True, max_length=255)
    value = models.CharField(max_length=255)
    ranking = models.IntegerField(null=True, blank=True, default=0, max_length=3, verbose_name="Ranking", help_text='A number from 0 to 999 to determine this object\'s position in a list.')
    active = models.BooleanField(help_text='Do you want the field to be visable on your form?', verbose_name='Is active?', default=True)
    tags = TagField()
    
    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['ranking']

#For making contacts for forms
class GenericContact(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=126)
    email = models.EmailField()
    
    class Meta:
        abstract = True
        ordering = ['last_name']
        
    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)
        
#For making a generic Contact form
class GenericContactForm(models.Model):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=255, verbose_name="Slug", unique=True)
    description = models.TextField('Form Description')
    form_class = models.CharField(max_length=255, verbose_name="Form Class name", unique=True)
    template = models.CharField(max_length=255)
    recipients = models.ManyToManyField(User, related_name='contact_form_recipients')
    is_public = models.BooleanField(default=True, help_text="Is the form available for public viewing?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
