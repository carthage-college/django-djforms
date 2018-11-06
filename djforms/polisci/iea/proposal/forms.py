from django import forms

from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.polisci.iea.proposal.models import ProposalContact
from djforms.core.models import REQ
from djtools.fields import STATE_CHOICES

from django_countries.widgets import CountrySelectWidget


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
        help_text = 'Choose "Other" if outside the United States',
        widget=forms.Select(choices=STATE_CHOICES, attrs=REQ)
    )

    class Meta:
        model = ProposalContact
        fields = (
            'first_name','last_name','email','address1','address2',
            'city','state','postal_code','country','phone','presenter_type',
            'affiliation','how_hear','abstract','submitting'
        )
        widgets = {'country': CountrySelectWidget}


class ProposalOrderForm(OrderForm):
    """
    Conference abstract proposal order form, extends
    base OrderForm in processors app
    """
    total = forms.CharField()

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')
