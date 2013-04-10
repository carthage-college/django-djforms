from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm, TrustCommerceForm, EXP_MONTH, EXP_YEAR

from djforms.lis.conferences.course_ference.models import CourseFerenceAttender, CourseFerenceVendor, SECTOR_CHOICES
from djforms.core.models import BINARY_CHOICES, STATE_CHOICES

from tagging.models import Tag, TaggedItem

FEE_CHOICES = (
    ("150","For profit: $150 vendor fee"),
    ("50","Not for profit: $50 vendor fee"),
)

class ProcessorForm(TrustCommerceForm):
    """
    Override generic form to add required attributes
    """
    billing_name        = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'class': 'required','required': 'required'}), label="Name on card")
    card_number         = forms.CharField(label="Card number", max_length=16, widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    expiration_month    = forms.CharField(max_length=2, widget=forms.Select(choices=EXP_MONTH,attrs={'class': 'required input-mini','required': 'required'}))
    expiration_year     = forms.CharField(max_length=4, widget=forms.Select(choices=EXP_YEAR,attrs={'class': 'required input-small','required': 'required'}))
    security_code       = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'class': 'required input-mini','required': 'required'}), required=True, help_text="The three or four digit security code on the back of your credit card.")


class AttenderContactForm(ContactForm):
    """
    LIS course-ference attender registration contact form, extends
    base ContactForm in processors app
    """
    first_name      = forms.CharField(max_length=128,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    last_name       = forms.CharField(max_length=128,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    email           = forms.CharField(max_length=75,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    address1        = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    city            = forms.CharField(max_length=128,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    state           = forms.CharField(widget=forms.Select(choices=STATE_CHOICES, attrs={'class': 'required','required': 'required'}))
    postal_code     = USZipCodeField(label="Zip code", widget=forms.TextInput(attrs={'class': 'required input-small','required': 'required','maxlength':'10'}))
    phone           = USPhoneNumberField(widget=forms.TextInput(attrs={'class': 'required','required': 'required','maxlength':'12'}))
    job_title       = forms.CharField(max_length=128,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    affiliation     = forms.CharField(label="Institution/Organization", max_length=256,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    
    class Meta:
        model       = CourseFerenceAttender
        fields      = ('first_name','last_name','email','address1','address2','city','state','postal_code','job_title','affiliation')


class AttenderOrderForm(OrderForm):
    """
    LIS course-ference attender registration order form, extends
    base OrderForm in processors app
    """
    total           = forms.CharField(widget=forms.HiddenInput(), initial="25.00")

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')


class VendorContactForm(ContactForm):
    """
    LIS course-ference vendor registration contact form, extends
    base ContactForm in processors app
    """
    first_name      = forms.CharField(max_length=128,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    last_name       = forms.CharField(max_length=128,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    email           = forms.CharField(max_length=75,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    address1        = forms.CharField(max_length=255,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    city            = forms.CharField(max_length=128,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    state           = forms.CharField(widget=forms.Select(choices=STATE_CHOICES, attrs={'class': 'required','required': 'required'}))
    postal_code     = USZipCodeField(label="Zip code", widget=forms.TextInput(attrs={'class': 'required input-small','required': 'required','maxlength':'10'}))
    phone           = USPhoneNumberField(widget=forms.TextInput(attrs={'class': 'required','required': 'required','maxlength':'12'}))
    affiliation     = forms.CharField(label="Institution/Organization", max_length=256,widget=forms.TextInput(attrs={'class': 'required','required': 'required'}))
    sector          = forms.CharField(widget=forms.Select(choices=SECTOR_CHOICES, attrs={'class': 'required','required': 'required'}))
    swag            = forms.CharField(widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs={'class': 'required','required': 'required'}), help_text="Are you able to possibly offer special opportunities, prizes, freebies to attendees (such as drawings, product previews, codes for a free item, etc?)")
    discussion      = forms.CharField(widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs={'class': 'required','required': 'required'}), help_text="Are you able to participate in either an online discussion forum or live chat to further enhance interaction with attendees?")

    class Meta:
        model       = CourseFerenceVendor
        fields      = ('affiliation', 'first_name','last_name','email','address1','address2','city','state','postal_code','phone','sector','swag','discussion')


class VendorOrderForm(OrderForm):
    """
    LIS course-ference vendor registration order form, extends
    base OrderForm in processors app
    """

    total           = forms.CharField(label="Type of Organization", widget=forms.RadioSelect(choices=FEE_CHOICES, attrs={'class': 'required','required': 'required'}))

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')