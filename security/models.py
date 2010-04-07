from django.db import models
from django.forms import ModelForm
from djforms.core.models import GenericContact, GenericChoice

from tagging.fields import TagField
from tagging.models import Tag

#Security Appeal Generic Model
class ParkingTicketAppeal(GenericContact):
    carthage_id        = models.CharField("Carthage ID#", max_length=10)
    residency_status   = models.ForeignKey(GenericChoice, related_name="security_appeal_residency_status")
    vehicle_make       = models.CharField("Vehicle Make", max_length=40)
    vehicle_model      = models.CharField("Vehicle Model", max_length=40)
    license_plate      = models.CharField("License Plate", max_length=20)
    state              = models.CharField("State", max_length=20)
    permit_type        = models.ForeignKey(GenericChoice, related_name="security_appeal_permit_type")
    permit_number      = models.CharField("Permit Number", max_length=30)
    citation_number    = models.CharField("Citation Number", max_length=30)
    appeal_box         = models.TextField("Comments", help_text="Please provide your comments in support of your appeal.")
