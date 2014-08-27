from django import forms

from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.polisci.wipcs.models import RegistrationContact, PAYMENT_CHOICES

from tagging.models import Tag, TaggedItem

FEE_CHOICES = (
    ("55","Faculty/Graduate student $55"),
    ("40","WIPCS member $40"),
    ("10","Undergraduate student $40")
)

class RegistrationContactForm(ContactForm):
    """
    WIPCS conference registration contact form, extends
    base ContactForm in processors app
    """

    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect()
    )

    class Meta:
        model = RegistrationContact
        fields = (
            'first_name','last_name','email','address1','address2',
            'city','state','postal_code','phone','how_hear','abstract',
            'cv','submitting','payment_method'
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

