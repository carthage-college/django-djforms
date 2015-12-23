from django import forms

from djforms.processors.models import Order
from djforms.polisci.iea.proposal.models import ProposalContact
from djforms.core.models import REQ, STATE_CHOICES
from localflavor.us.forms import USPhoneNumberField, USZipCodeField

from tagging.models import Tag, TaggedItem


class ProposalContactForm(forms.ModelForm):
    """
    WIPCS conference proposal form
    """
    address1 = forms.CharField(
        max_length=255,widget=forms.TextInput(attrs=REQ)
    )
    city = forms.CharField(
        max_length=128,widget=forms.TextInput(attrs=REQ)
    )
    state = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES, attrs=REQ)
    )
    postal_code = USZipCodeField(
        label="Zip code",
        widget=forms.TextInput(
            attrs={'class': 'required input-small','maxlength':'10'}
        )
    )
    phone = USPhoneNumberField(
        widget=forms.TextInput(attrs=REQ)
    )

    class Meta:
        model = ProposalContact
        fields = (
            'first_name','last_name','email','address1','address2',
            'city','state','postal_code','phone','presenter_type',
            'affiliation','how_hear','abstract','submitting'
        )

