from django import forms
from djforms.security.models import ParkingTicketAppeal
from tagging.models import Tag, TaggedItem
from djforms.core.models import STATE_CHOICES, GenericChoice

try:
    status_tag = Tag.objects.get(name='Residency Status')
    RESIDENCY_STATUS = TaggedItem.objects.get_by_model(GenericChoice, status_tag).filter(active = True)
except:
    RESIDENCY_STATUS = GenericChoice.objects.none()

try:
    type_tag = Tag.objects.get(name='Permit Type')
    PERMIT_TYPE = TaggedItem.objects.get_by_model(GenericChoice, type_tag).filter(active = True)
except:
    PERMIT_TYPE = GenericChoice.objects.none()

class ParkingTicketAppealForm(forms.ModelForm):
    state   = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=True)
    residency_status = forms.ModelChoiceField(queryset=RESIDENCY_STATUS, empty_label=None, widget=forms.RadioSelect())
    permit_type = forms.ModelChoiceField(queryset=PERMIT_TYPE, widget=forms.Select(),empty_label='Select Permit')

    class Meta:
        model = ParkingTicketAppeal
