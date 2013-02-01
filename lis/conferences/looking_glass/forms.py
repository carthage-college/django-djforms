from django import forms

from djforms.core.models import GenericChoice
from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.lis.conferences.looking_glass.models import RegistrationContact

from tagging.models import Tag, TaggedItem

FEE_CHOICES = (
    ("65","Regular Rate $65"),
    ("40","Student Rate $40"),
)


class RegistrationContactForm(ContactForm):
    """
    LIS conference registration contact form, extends
    base ContactForm in processors app
    """

    def __init__(self, *args, **kwargs):
        super(RegistrationContactForm,self).__init__(*args, **kwargs)
        self.fields.pop('phone')

    class Meta:
        model       = RegistrationContact
        fields      = ('first_name','last_name','email','address1','address2','city','state','postal_code','name_tag','affiliation','dietary_needs','other_needs')

class RegistrationOrderForm(OrderForm):
    """
    LIS conference registration order form, extends
    base OrderForm in processors app
    """
    total           = forms.CharField(label="Conference Fee", widget=forms.RadioSelect(choices=FEE_CHOICES))

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')

