from django.db import models
from django.forms import ModelForm
from djforms.core.models import GenericContact, GenericChoice

from django.contrib.auth.models import User

from tagging.fields import TagField
from tagging.models import Tag

#Adult edu profile form
class EduProfile(GenericContact):
    phone = models.CharField(max_length=30, verbose_name='Phone Number')
    address = models.TextField(verbose_name='mailing Address')
    #The fields of Generic choice types, linked to core
    contact_time = models.ForeignKey(GenericChoice, related_name="edu_profile_contact_time")
    academic_programs = models.ManyToManyField(GenericChoice, related_name="edu_profile_academic_programs") 
    how_did_you_hear_about_us = models.ForeignKey(GenericChoice, related_name="edu_profile_how_did_you_hear_about_us")
    hear_about_us_other = models.TextField(blank=True, verbose_name='If other, Please Specify.')
    
    def render_email(self):
        obj_text = 'First Name:    %s\n' % self.first_name
        obj_text += 'Last Name:    %s\n' % self.last_name
        obj_text += 'Email:     %s\n' % self.email
        obj_text += 'Phone:    %s\n' % self.phone
        obj_text += '\nMailing Address:\n\n%s\n\n' % self.address
        
        obj_text += 'Best time to contact is in the %s \n' % self.contact_time
        
        obj_text += '\n\nAcademic Programs of Interest:\n\n'
        for poi in self.academic_programs.all():
            obj_text += "    " + poi.name + "\n"
            
        obj_text += '\nHeard about us through %s\n' % self.how_did_you_hear_about_us
            
        obj_text += '\nHow they heard about us "other" field contained:\n\n'+ '    ' + '%s\n' % self.hear_about_us_other

        return obj_text
