from django.db import models
from django.forms import ModelForm
from djforms.core.models import GenericContact, GenericChoice

from django.contrib.auth.models import User

from tagging.fields import TagField
from tagging.models import Tag

#Maintenance Request model
class MaintenanceRequest(GenericContact):
    phone               = models.CharField(max_length=30, verbose_name='Phone Number')
    type_of_request     = models.ForeignKey(GenericChoice, related_name="maintenance_request_type_of_request")
    building_name       = models.ForeignKey(GenericChoice, related_name="maintenance_request_building_name")
    residence_hall      = models.ForeignKey(GenericChoice, related_name="maintenance_request_residence_hall")
    room_number         = models.CharField(max_length=3, verbose_name='Room Number')
    floor               = models.ForeignKey(GenericChoice, related_name="maintenance_request_floor")
    floor_other         = models.TextField(blank=True, verbose_name='If other, Please Specify.')
    wing                = models.ForeignKey(GenericChoice, related_name="maintenance_request_wing")
    problem_description = models.TextField(blank=True, verbose_name='Please explain the nature of the problem.')
    
    def render_email(self):
        obj_text += 'Date request made:  %s\n' % self.creation_date
        obj_text =  'First Name:         %s\n' % self.first_name
        obj_text += 'Last Name:          %s\n' % self.last_name
        obj_text += 'Email:              %s\n' % self.email
        obj_text += 'Phone:              %s\n' % self.phone
        obj_text += 'Type of request:    %s\n' % self.type_of_request
        obj_text += 'Building Name:      %s\n' % self.building_name
        obj_text += 'Residence Hall:     %s\n' % self.residence_hall
        obj_text += 'Room Number:        %s\n' % self.room_number
        obj_text += 'Floor:              %s\n' % self.floor
        obj_text += 'Floor other Field:  %s\n' % self.floor_other
        obj_text += 'Wing:               %s\n' % self.wing
        obj_text += '\nDescription of the problem:\n\n%s\n' % self.problem_description
        return obj_text


