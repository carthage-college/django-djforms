from django.db import models
from djforms.core.models import GenericChoice

from django.contrib.auth.models import User

STATUS_CHOICES = (
    ('New', 'New'),
    ('In Progress', 'In Progress'),
    ('Replaced', 'Replaced'),
    ('Fixed', 'Fixed'),
    ('Cleaned', 'Cleaned'),
    ('Complete', 'Complete'),
)

class MaintenanceRequest(models.Model):

    user                = models.ForeignKey(User, verbose_name="Created by", related_name="maintenance_request_user")
    updated_by          = models.ForeignKey(User, verbose_name="Updated by", related_name="maintenance_request_updated_by", null=True, blank=True, editable=False)
    date_created        = models.DateTimeField("Date Created", auto_now_add=True)
    date_completed      = models.DateTimeField("Date Completed", null=True, blank=True, help_text="Format: yyyy-mm-dd")
    type_of_request     = models.ForeignKey(GenericChoice, help_text="Need type of request definitions here.", related_name="maintenance_request_type_of_request")
    status              = models.CharField("Status of request", max_length=100, choices=STATUS_CHOICES)
    building            = models.ForeignKey(GenericChoice, verbose_name="Building Name", help_text="Name of the building on campus", related_name="maintenance_request_building")
    room_number         = models.CharField("Room Number or Location", max_length=50, help_text="If location, use: Lounge, restrooms, common area, lobby, hallway, foyer, etc. ")
    floor               = models.CharField("Floor Number", max_length=2, help_text='Use "0" for "basement"' )
    description         = models.TextField("Description", help_text="Please explain the nature of the problem.")
    notes               = models.TextField("Notes", help_text="Staff can provide further information here.", null=True, blank=True)
    damage_charge       = models.CharField("Damage Charge", max_length=16, null=True, blank=True)

    class Meta:
        permissions = ( ("can_manage", "Manage"),("can_view","View"), )
        ordering  = ('-date_created',)
        get_latest_by = 'date_created'

    @models.permalink
    def get_absolute_url(self):
        return ('maintenance_request_detail', [str(self.id)])

    @models.permalink
    def get_update_url(self):
        return ('maintenance_request_update', [str(self.id)])

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def phone(self):
        return self.user.get_profile().phone

    def building_name(self):
        return self.building.name

    def render_email(self):
        obj_text  = 'Date of request:    %s\n' % self.date_created
        obj_text += 'First Name:         %s\n' % self.user.first_name
        obj_text += 'Last Name:          %s\n' % self.user.last_name
        obj_text += 'Email:              %s\n' % self.user.email
        obj_text += 'Phone:              %s\n' % self.user.get_profile().phone
        obj_text += 'Type of request:    %s\n' % self.type_of_request
        obj_text += 'Building Name:      %s\n' % self.building.name
        obj_text += 'Room Number:        %s\n' % self.room_number
        obj_text += 'Floor:              %s\n' % self.floor
        obj_text += '\nDescription of the problem:\n\n%s\n' % self.description
        return obj_text
