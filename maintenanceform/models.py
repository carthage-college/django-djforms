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
    
xName (preferrably their Novell Login)

xPhone Number

xDate (time stamped so individual cannot back date a request)

xType of Request
    Maintenance Request (Dave Perttula manages)
    Environmental Services Request (Mary Slater manages)
    Laundry/Time Warner Cable Request (Amanda Binger manages)

xBuilding Name
    CC - A.W. Clausen Center for World Business
    DSC - David A. Straz, Jr. Center for the Natural and Social Sciences
    JAC - H. F. Johnson Center for the Fine Arts
    HL - Hedberg Library
    LH - Lentz Hall
    SIE - A. F. Siebert Chapel
    SN - W.A. Seidemann Natatorium
    TARC - N.E. Tarble Athletic Recreation Center
    TWC - Todd Wehr Center

xResidence Hall
    DEN - Henry Denhart Residence Hall (Rebekah Hughes has viewing access)
    JOH - Joseph Johnson Residence Hall (Diana Garner has viewing access)
    OAKA - Oaks A Residence Hall (Holly Rodden has viewing access)
    OAKB - Oaks B Residence Hall (Holly Rodden has viewing access)
    OAKC - Oaks C Residence Hall (Holly Rodden has viewing access)
    OAKD - Oaks D Residence Hall (Holly Rodden has viewing access)
    SOU - South Residence Hall (Nina Caliguiri has viewing access)
    SW - Swenson Hall (Amanda Binger has viewing access)
    TAR - Pat Tarble Residence Hall (Amanda Binger has viewing access)

xRoom Number

xFloor
    Basement
    First Floor
    Second Floor
    Third Floor
    Fourth Floor
    Fifth Floor
    Other 

x(with option to fill in the blank)

xWing
    Wing A
    Wing B
    Tarble Short
    Tarble Long
    Not Applicable

xDescription Box for problem


We would need something that states it will take a minimum of 48 hours
to address a situation.  Please list the Dean of Students Office as an
emergency contact number as well.  Let me know if you need more
wording/text and I would be happy to supply.  Thanks again!!!

