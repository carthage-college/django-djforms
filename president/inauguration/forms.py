from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from djforms.president.inauguration.models import RsvpContact
from djforms.core.models import STATE_CHOICES, YEARS1, BINARY_CHOICES

class RsvpForm(forms.ModelForm):
    first_name      = forms.CharField(label="Delegate's first name")
    last_name       = forms.CharField(label="Delegate's last name")
    email           = forms.EmailField()
    state           = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=False)
    postal_code     = USZipCodeField(label="Zip code")
    phone           = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    march           = forms.ChoiceField(label="Delegate will march in the academic procession", choices=BINARY_CHOICES, widget=forms.RadioSelect())
    attend          = forms.ChoiceField(label="I will attend the Inaugural Luncheon", choices=BINARY_CHOICES, widget=forms.RadioSelect())
    guest_attend    = forms.ChoiceField(label="My guest will also attend this event", choices=BINARY_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model       = RsvpContact
        exclude     = ('created_at','updated_at',)
        fields      = ('institution','year_founded','first_name','last_name','job_title','degree','cohort','address1','address2','city','state','postal_code','phone','email','march','attend','guest_attend')

