from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from djforms.president.inauguration.models import RsvpContact
from djforms.core.models import STATE_CHOICES, YEARS1, BINARY_CHOICES

class RsvpForm(forms.ModelForm):
    email           = forms.EmailField()
    state           = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=False)
    postal_code     = USZipCodeField(label="Zip Code")
    phone           = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    year_founded    = forms.CharField("Year Founded", widget=forms.Select(choices=YEARS1))
    march           = forms.ChoiceField(label="Delegate will march in the academic procession", choices=BINARY_CHOICES, widget=forms.RadioSelect())
    attend          = forms.ChoiceField(label="I will attend the Inaugural Luncheon", choices=BINARY_CHOICES, widget=forms.RadioSelect())
    guest_attend    = forms.ChoiceField(label="My guest will also attend this event", choices=BINARY_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = RsvpContact
        exclude = ('created_at','updated_at',)
