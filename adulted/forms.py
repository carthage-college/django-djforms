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
    birth_city          = forms.CharField(max_length=128)
    birth_state         = forms.CharField(widget=forms.Select(choices=STATE_CHOICES))
    birth_country       = forms.CharField(widget=forms.Select(choices=COUNTRIES))

class EmploymentForm(forms.Form):
    """
    employment history
    """
    # current employment
    employer            = forms.CharField(max_length=128, required=False)
    position            = forms.CharField(max_length=128, required=False)
    tuition_reimburse   = forms.TypedChoiceField(widget=forms.RadioSelect(choices=BINARY_CHOICES), label="Does your employer offer tuition reimbursement?")
    # employment history
    past_employer1      = forms.CharField(max_length=128, required=False)
    past_position1      = forms.CharField(max_length=128, required=False)
    past_dates1         = forms.CharField(max_length=128, required=False)
    past_employer2      = forms.CharField(max_length=128, required=False)
    past_position2      = forms.CharField(max_length=128, required=False)
    past_dates2         = forms.CharField(max_length=128, required=False)
    past_employer3      = forms.CharField(max_length=128, required=False)
    past_position3      = forms.CharField(max_length=128, required=False)
    past_dates3         = forms.CharField(max_length=128, required=False)

class EducationForm(forms.Form):
    """
    education background
    """
    # high schools and colleges
    school1             = forms.CharField(max_length=128, required=False, label="School")
    location1           = forms.CharField(max_length=128, required=False, label="Location")
    dip_degree1         = forms.CharField(max_length=128, required=False, label="Diploma/Degree")
    attend1             = forms.CharField(max_length=128, required=False, label="Dates attended")
    school2             = forms.CharField(max_length=128, required=False, label="School")
    location2           = forms.CharField(max_length=128, required=False, label="Location")
    dip_degree2         = forms.CharField(max_length=128, required=False, label="Diploma/Degree")
    attend2             = forms.CharField(max_length=128, required=False, label="Dates attended")
    school3             = forms.CharField(max_length=128, required=False, label="School")
    location3           = forms.CharField(max_length=128, required=False, label="Location")
    dip_degree3         = forms.CharField(max_length=128, required=False, label="Diploma/Degree")
    attend3             = forms.CharField(max_length=128, required=False, label="Dates attended")
    school4             = forms.CharField(max_length=128, required=False, label="School")
    location4           = forms.CharField(max_length=128, required=False, label="Location")
    dip_degree4         = forms.CharField(max_length=128, required=False, label="Diploma/Degree")
    attend4             = forms.CharField(max_length=128, required=False, label="Dates attended")
    school5             = forms.CharField(max_length=128, required=False, label="School")
    location5           = forms.CharField(max_length=128, required=False, label="Location")
    dip_degree5         = forms.CharField(max_length=128, required=False, label="Diploma/Degree")
    attend5             = forms.CharField(max_length=128, required=False, label="Dates attended")
    military_service    = forms.CharField(widget=forms.Select(choices=BINARY_CHOICES), label="Have you ever served in the military?")
    statement           = forms.CharField(widget=forms.Textarea)
    payment_method      = forms.CharField(widget=forms.Select(choices=PAYMENT_CHOICES))
