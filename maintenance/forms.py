from django import forms
from django.forms import ModelForm
from djforms.maintenance.models import MaintenanceRequest
from tagging.models import Tag, TaggedItem
from djforms.core.models import GenericChoice

try:
    type_of_request_tag = Tag.objects.get(name__iexact='Maintenance Request Type')
    TYPE_OF_REQUEST = TaggedItem.objects.get_by_model(GenericChoice, type_of_request_tag).filter(active=True)
except:
    TYPE_OF_REQUEST = GenericChoice.objects.none()

try:
    building_name_tag = Tag.objects.get(name__iexact='Building Name')
    BUILDING_NAME = TaggedItem.objects.get_by_model(GenericChoice, building_name_tag).filter(active=True)
except:
    BUILDING_NAME = GenericChoice.objects.none()

class EVSForm(forms.ModelForm):
    type_of_request = forms.ModelChoiceField(queryset=TYPE_OF_REQUEST, help_text="Need 'type of request' definitions here.")
    building = forms.ModelChoiceField(queryset=BUILDING_NAME, label="Building Name")

    class Meta:
        model = MaintenanceRequest
        exclude = ('user','date_completed','status','damage_charge','notes', 'updated_by')

    def clean_floor(self):
        """
        insure that the floor is an integer
        """
        try:
            floor = int(self.cleaned_data['floor'].strip().split()[0])
        except (ValueError, IndexError):
            raise forms.ValidationError("Floor number should be an integer")

        return floor

class EVSFormUpdate(forms.ModelForm):
    type_of_request = forms.ModelChoiceField(queryset=TYPE_OF_REQUEST)
    building = forms.ModelChoiceField(queryset=BUILDING_NAME)

    class Meta:
        model = MaintenanceRequest
        exclude = ('user', 'updated_by')

    def clean_floor(self):
        """
        insure that the floor is an integer
        """
        try:
            floor = int(self.cleaned_data['floor'].strip().split()[0])
        except (ValueError, IndexError):
            raise forms.ValidationError("Floor number should be an integer")

        return floor
