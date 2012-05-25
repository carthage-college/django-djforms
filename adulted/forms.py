from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField, USSocialSecurityNumberField

from djforms.core.models import GENDER_CHOICES, STATE_CHOICES, COUNTRIES, BINARY_CHOICES, PAYMENT_CHOICES
from djforms.processors.models import Contact, Order
from djforms.adulted.models import Admissions

class ContactForm(forms.ModelForm):
    """
    Contact form based on the generic processor model
    """
    previous_last       = forms.CharField(max_length=128, required=False, label="Previous Last Name")
    phone               = USPhoneNumberField(max_length=12, help_text="Format: XXX-XXX-XXXX")
    state               = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=True)
    postal_code         = USZipCodeField(label="Zip")

    class Meta:
        model = Contact

class PersonalForm(forms.Form):
    """
    personal data
    """
    gender              = forms.TypedChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    ss_num              = USSocialSecurityNumberField(label="Social security number")
    dob                 = forms.DateField(label = "Date of birth", help_text="Format: dd/mm/yyyy")
    pob                 = forms.CharField(max_length=128, label="Place of birth", help_text="(City, State, Country)")

class EmploymentForm(forms.Form):
    """
    employment history
    """
    # current employment
    employer            = forms.CharField(max_length=128, required=False)
    position            = forms.CharField(max_length=128, required=False)
    tuition_reimburse   = forms.TypedChoiceField(widget=forms.RadioSelect(choices=BINARY_CHOICES), label="Does your employer offer tuition reimbursement?")

