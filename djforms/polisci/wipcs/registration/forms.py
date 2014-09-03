from django import forms

from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.polisci.wipcs.registration.models import RegistrationContact
from djforms.polisci.wipcs.registration.models import PAYMENT_CHOICES
from djforms.core.models import REQ, STATE_CHOICES
from localflavor.us.forms import USPhoneNumberField, USZipCodeField

from tagging.models import Tag, TaggedItem

FEE_CHOICES = (
    ("55","Faculty/Graduate student $55"),
    ("45","WIPCS member $45"),
    ("10","Undergraduate student $10")
)

class RegistrationContactForm(ContactForm):
    """
    WIPCS conference registration contact form, extends
    base ContactForm in processors app
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
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect()
    )

    class Meta:
        model = RegistrationContact
        fields = (
            'first_name','last_name','email','address1','address2',
            'city','state','postal_code','phone','how_hear',
            'payment_method'
        )

class RegistrationOrderForm(OrderForm):
    """
    LIS conference registration order form, extends
    base OrderForm in processors app
    """
    total = forms.CharField(
        label="Conference Fee",
        widget=forms.RadioSelect(choices=FEE_CHOICES)
    )

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')

