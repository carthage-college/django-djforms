from django import forms

from djforms.processors.models import Order
from djforms.polisci.wipcs.proposal.models import ProposalContact
from djforms.core.models import REQ, STATE_CHOICES
from localflavor.us.forms import USPhoneNumberField, USZipCodeField

from tagging.models import Tag, TaggedItem

FEE_CHOICES = (
    ("55","Faculty/Graduate student $55"),
    ("40","WIPCS member $40"),
    ("10","Undergraduate student $40")
)

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
    cv = forms.FileField(
        label="CV", max_length="256"
    )

    class Meta:
        model = ProposalContact
        fields = (
            'first_name','last_name','email','address1','address2',
            'city','state','postal_code','phone','how_hear','abstract',
            'cv','submitting'
        )

