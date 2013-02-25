from django import forms

from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.lis.conferences.course_ference.models import CourseFerenceRegistration

from tagging.models import Tag, TaggedItem

class RegistrationContactForm(ContactForm):
    """
    LIS course-ference registration contact form, extends
    base ContactForm in processors app
    """

    class Meta:
        model       = CourseFerenceRegistration
        fields      = ('first_name','last_name','email','address1','address2','city','state','postal_code','job_title','affiliation')

class RegistrationOrderForm(OrderForm):
    """
    LIS course-ference registration order form, extends
    base OrderForm in processors app
    """
    total           = forms.CharField(widget=forms.HiddenInput(), initial="25.00")

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')

