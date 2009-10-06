from django import forms
from django.db import models
from django.forms import ModelForm
from djforms.maintenanceform.models import MaintenanceRequest
from tagging.models import Tag, TaggedItem
from djforms.core.models import GenericContact, GenericChoice

#Sets up and populates the many to many fields on the EduProfileForm based on entries in Generic Choice and their tags
try:
    type_of_request_tag = Tag.objects.get(name__iexact='Type Of Request')
    TYPE_OF_REQUEST = TaggedItem.objects.get_by_model(GenericChoice, type_of_request_tag).filter(active = True)
except:
    TYPE_OF_REQUEST = GenericChoice.objects.none()

try:
    building_name_tag = Tag.objects.get(name__iexact='Building Name')
    BUILDING_NAME = TaggedItem.objects.get_by_model(GenericChoice, building_name_tag).filter(active = True)
except:
    BUILDING_NAME = GenericChoice.objects.none()

try:
    residence_hall_tag = Tag.objects.get(name__iexact='Residence Hall')
    RESIDENCE_HALL = TaggedItem.objects.get_by_model(GenericChoice, residence_hall_tag).filter(active = True)
except:
    RESIDENCE_HALL = GenericChoice.objects.none()

try:
    floor_tag = Tag.objects.get(name__iexact='Floor')
    FLOOR = TaggedItem.objects.get_by_model(GenericChoice, floor_tag).filter(active = True)
except:
    FLOOR = GenericChoice.objects.none()
    
try:
    wing_tag = Tag.objects.get(name__iexact='Wing')
    WING = TaggedItem.objects.get_by_model(GenericChoice, wing_tag).filter(active = True)
except:
    WING = GenericChoice.objects.none()

class MaintenanceEVSForm(forms.ModelForm):
    type_of_request = forms.ModelChoiceField(queryset=TYPE_OF_REQUEST, empty_label=None)
    building_name   = forms.ModelChoiceField(queryset=BUILDING_NAME, empty_label=None)
    residence_hall  = forms.ModelChoiceField(queryset=RESIDENCE_HALL, empty_label=None)
    floor           = forms.ModelChoiceField(queryset=FLOOR, empty_label=None)
    wing            = forms.ModelChoiceField(queryset=WING, empty_label=None)
    
    class Meta:
        model = MaintenanceRequest
