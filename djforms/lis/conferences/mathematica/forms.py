from django import forms

from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.lis.conferences.mathematica.models import Registration
from djforms.core.models import REQ, STATE_CHOICES

from localflavor.us.forms import USPhoneNumberField, USZipCodeField


FEE_CHOICES = (
    ("30","$30 for individual registration"),
    ("40","$40 for individual registration  (after July 15)"),
    (
        "100",
        """
            $100 group discount for groups of four or more
            (must all be from the same institution)
        """
    ),
)

class RegistrationForm(ContactForm):
    """
    LIS mathematica conference registration contact form, extends
    base ContactForm in processors app
    """
    first_name = forms.CharField(
        max_length=128,widget=forms.TextInput(attrs=REQ)
    )
    last_name = forms.CharField(
        max_length=128,widget=forms.TextInput(attrs=REQ)
    )
    email = forms.CharField(
        max_length=128,widget=forms.TextInput(attrs=REQ)
    )
    job_title = forms.CharField(
        max_length=128,widget=forms.TextInput(attrs=REQ)
    )
    department = forms.CharField(
        max_length=128,widget=forms.TextInput(attrs=REQ)
    )
    affiliation = forms.CharField(
        label="Institution/Organization",
        max_length=256,widget=forms.TextInput(attrs=REQ)
    )
    address1 = forms.CharField(
        label = "Address",
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

    class Meta:
        model = Registration
        fields = (
            'first_name','last_name','email','job_title','department',
            'affiliation','address1','city','state','postal_code',
            'phone','group_members'
        )


class RegistrationOrderForm(OrderForm):
    """
    LIS mathematica attender registration order form, extends
    base OrderForm in processors app
    """

    total = forms.CharField(
        label="Conference Fee",
        widget=forms.RadioSelect(choices=FEE_CHOICES)
    )

    class Meta:
        model = Order
        fields = ('total','avs','auth')
