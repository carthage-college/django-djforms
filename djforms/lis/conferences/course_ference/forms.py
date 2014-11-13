from django import forms

from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm, TrustCommerceForm
from djforms.lis.conferences.course_ference.models import CourseFerenceAttender, CourseFerenceVendor, SECTOR_CHOICES
from djforms.core.models import BINARY_CHOICES, STATE_CHOICES, REQ

from localflavor.us.forms import USPhoneNumberField, USZipCodeField

FEE_CHOICES = (
    ("150","For profit: $150 vendor fee"),
    ("50","Not for profit: $50 vendor fee"),
)

class AttenderContactForm(forms.ModelForm):
    """
    LIS course-ference attender registration contact form, extends
    base ContactForm in processors app
    """
    first_name      = forms.CharField(max_length=128,widget=forms.TextInput(attrs=REQ))
    last_name       = forms.CharField(max_length=128,widget=forms.TextInput(attrs=REQ))
    email           = forms.CharField(max_length=75,widget=forms.TextInput(attrs=REQ))
    job_title       = forms.CharField(max_length=128,widget=forms.TextInput(attrs=REQ))
    affiliation     = forms.CharField(label="Institution/Organization", max_length=256,widget=forms.TextInput(attrs=REQ))

    class Meta:
        model       = CourseFerenceAttender
        fields      = ('first_name','last_name','email','job_title','affiliation')

class AttenderContactForm2(forms.ModelForm):
    """
    LIS course-ference attender registration contact form, extends
    base ContactForm in processors app
    """
    first_name      = forms.CharField(max_length=128)
    last_name       = forms.CharField(max_length=128)
    email           = forms.CharField(max_length=75)
    job_title       = forms.CharField(max_length=128)
    affiliation     = forms.CharField(label="Institution/Organization", max_length=256)

    class Meta:
        model       = CourseFerenceAttender
        fields      = ('first_name','last_name','email','job_title','affiliation')

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
    first_name      = forms.CharField(max_length=128,widget=forms.TextInput(attrs=REQ))
    last_name       = forms.CharField(max_length=128,widget=forms.TextInput(attrs=REQ))
    email           = forms.CharField(max_length=75,widget=forms.TextInput(attrs=REQ))
    address1        = forms.CharField(max_length=255,widget=forms.TextInput(attrs=REQ))
    city            = forms.CharField(max_length=128,widget=forms.TextInput(attrs=REQ))
    state           = forms.CharField(widget=forms.Select(choices=STATE_CHOICES, attrs=REQ))
    postal_code     = USZipCodeField(label="Zip code", widget=forms.TextInput(attrs={'class':'required input-small','required':'required','maxlength':'10'}))
    phone           = USPhoneNumberField(widget=forms.TextInput(attrs={'class':'required','required':'required','maxlength':'12'}))
    affiliation     = forms.CharField(label="Institution/Organization",max_length=256,widget=forms.TextInput(attrs=REQ))
    sector          = forms.CharField(widget=forms.Select(choices=SECTOR_CHOICES, attrs=REQ))
    description     = forms.CharField(widget=forms.Textarea(attrs={'class':'required','required':'required','rows':'5'}),label="Resources/Materials",required=True,help_text="Provide a brief description of the resources/materials you provide to libraries.")
    swag            = forms.CharField(widget=forms.RadioSelect(choices=BINARY_CHOICES, attrs=REQ), help_text="Are you able to possibly offer special opportunities, prizes, freebies to attendees (such as drawings, product previews, codes for a free item, etc?)")
    discussion      = forms.CharField(widget=forms.RadioSelect(choices=BINARY_CHOICES,attrs=REQ),help_text="Are you able to participate in either an online discussion forum or live chat to further enhance interaction with attendees?")

    class Meta:
        model       = CourseFerenceVendor
        fields      = ('affiliation', 'first_name','last_name','email','address1','address2','city','state','postal_code','phone','sector','description','swag','discussion')


class VendorOrderForm(OrderForm):
    """
    LIS course-ference vendor registration order form, extends
    base OrderForm in processors app
    """

    total           = forms.CharField(label="Type of Organization", widget=forms.RadioSelect(choices=FEE_CHOICES, attrs=REQ))

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')
