from django import forms

from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.lis.conferences.course_ference.models import CourseFerenceRegistration

from tagging.models import Tag, TaggedItem

class AttenderContactForm(ContactForm):
    """
    LIS course-ference attender registration contact form, extends
    base ContactForm in processors app
    """

    class Meta:
        model       = CourseFerenceRegistration
        fields      = ('first_name','last_name','email','address1','address2','city','state','postal_code','job_title','affiliation')

class AttenderOrderForm(OrderForm):
    """
    LIS course-ference attender registration order form, extends
    base OrderForm in processors app
    """

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')

"""
Areyou able to possibly offer special opportunities, prizes, freebies to attendees (such as drawings, product previews, codes for a free item, etc?)
(check box) Yes / No

Are you able to participate in either an online discussion forum or live chat to further enhance interaction with attendees?
(Check box) Yes / No
"""

