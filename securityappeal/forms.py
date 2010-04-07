from django import forms
from djforms.securityappeal.models import *
from tagging.models import Tag, TaggedItem
from djforms.core.models import STATE_CHOICES

#Sets up and populates the many to many fields on the SecurityAppealForm based on entries in Generic Choice and their tags
RESIDENCY_STATUS = []
try:
    status_tag = Tag.objects.get(name='Residency Status')
    RESIDENCY_STATUS = TaggedItem.objects.get_by_model(GenericChoice, status_tag).filter(active = True)
except:
    pass

PERMIT_TYPE = []
try:
    type_tag = Tag.objects.get(name='Permit Type')
    PERMIT_TYPE = TaggedItem.objects.get_by_model(GenericChoice, type_tag).filter(active = True)
except:
    pass

class SecurityAppealForm(forms.ModelForm):
    state   = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=True)
    residency_status = forms.ModelChoiceField(queryset=RESIDENCY_STATUS, empty_label=None, widget=forms.RadioSelect())
    permit_type = forms.ModelChoiceField(queryset=PERMIT_TYPE, widget=forms.Select(),empty_label='Select Permit')
    
    class Meta:
        model = SecurityAppeal
