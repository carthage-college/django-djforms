from django import forms

from djforms.core.models import GenericChoice
from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.lis.conferences.registration.models import RegistrationContact

from tagging.models import Tag, TaggedItem

try:
    events_tag      = Tag.objects.get(name__iexact='LIS Conference Events')
    EVENTS          = TaggedItem.objects.get_by_model(GenericChoice, events_tag).filter(active=True).order_by("name")
except:
    EVENTS          = GenericChoice.objects.none()


class RegistrationContactForm(ContactForm):
    """
    LIS conference registration contact form, extends
    base ContactForm in processors app
    """
    event           = forms.ModelMultipleChoiceField(queryset=EVENTS, widget=forms.CheckboxSelectMultiple(), required=True)

    class Meta:
        model       = RegistrationContact
        fields      = ('first_name','last_name','email','phone','address1','address2','city','state','postal_code','name_tag','affiliation','dietary_needs','other_needs','housing','event')

class RegistrationOrderForm(OrderForm):
    """
    LIS conference registration order form, extends
    base OrderForm in processors app
    """
    total           = forms.CharField(label="Amount",)

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')

