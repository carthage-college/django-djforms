from django import forms
from djforms.core.models import STATE_CHOICES

from localflavor.us.forms import USPhoneNumberField, USZipCodeField

NOMINATED_FOR =  [
    (
        'Distinguished Alumni Achievement Award',
        'Distinguished Alumni Achievement Award'
    ),
    (
        'Distinguished Alumni Service Award ',
        'Distinguished Alumni Service Award '
    ),
]

class NomineeForm(forms.Form):
    name = forms.CharField(label="Name")
    year = forms.IntegerField(label="Class Year")
    address = forms.CharField(label="Street Address")
    city = forms.CharField(label="City")
    state = forms.CharField(
        label="State", widget=forms.Select(choices=STATE_CHOICES)
    )
    postal_code = USZipCodeField(label="Zip Code")
    phone = USPhoneNumberField(label="Phone", max_length=12)
    email = forms.EmailField()
    nominated = forms.TypedChoiceField(
        label="Nominated For", choices=NOMINATED_FOR,
        widget=forms.RadioSelect()
    )
    description = forms.CharField(
        label="Information Background on Nominee", widget=forms.Textarea
    )

class NominatorForm(NomineeForm):

    def __init__(self, *args, **kwargs):
        super(NominatorForm, self).__init__(*args, **kwargs)
        # don't show the following fields
        del self.fields['description']
        del self.fields['nominated']
