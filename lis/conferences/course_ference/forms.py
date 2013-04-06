from django import forms

from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.lis.conferences.course_ference.models import CourseFerenceAttender, CourseFerenceVendor
from djforms.core.models import BINARY_CHOICES

from tagging.models import Tag, TaggedItem

FEE_CHOICES = (
    ("150","For profit: $150 vendor fee"),
    ("50","Not for profit: $50 vendor fee"),
)

class AttenderContactForm(ContactForm):
    """
    LIS course-ference attender registration contact form, extends
    base ContactForm in processors app
    """

    class Meta:
        model       = CourseFerenceAttender
        fields      = ('first_name','last_name','email','address1','address2','city','state','postal_code','job_title','affiliation')

class AttenderOrderForm(OrderForm):
    """
    LIS course-ference attender registration order form, extends
    base OrderForm in processors app
    """

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')

class VendorContactForm(ContactForm):
    """
    LIS course-ference vendor registration contact form, extends
    base ContactForm in processors app
    """

    swag                = forms.CharField(widget=forms.RadioSelect(choices=BINARY_CHOICES), help_text="Are you able to possibly offer special opportunities, prizes, freebies to attendees (such as drawings, product previews, codes for a free item, etc?)")
    discussion          = forms.CharField(widget=forms.RadioSelect(choices=BINARY_CHOICES), help_text="Are you able to participate in either an online discussion forum or live chat to further enhance interaction with attendees?")

    class Meta:
        model       = CourseFerenceVendor
        fields      = ('affiliation', 'first_name','last_name','email','address1','address2','city','state','postal_code','phone','sector','swag','discussion')

class VendorOrderForm(OrderForm):
    """
    LIS course-ference vendor registration order form, extends
    base OrderForm in processors app
    """

    total           = forms.CharField(label="Type of Organization", widget=forms.RadioSelect(choices=FEE_CHOICES))

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')

