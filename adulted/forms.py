from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField, USSocialSecurityNumberField

from djforms.core.models import GENDER_CHOICES, STATE_CHOICES, COUNTRIES, BINARY_CHOICES, PAYMENT_CHOICES
from djforms.processors.models import Contact, Order
from djforms.adulted.models import Admissions

import datetime
NOW    = datetime.datetime.now()
MONTH  = int(NOW.month)
YEAR   = int(NOW.year)
YEAR7  = YEAR
YEAR14 = YEAR

EDUCATION_GOAL = (
    (1,"I would like to earn my first bachelor's degree."),
    (6,"I already have a bachelor's degree and now would like to complete an additional major."),
    (7,"I would like to take classes for my own personal interest."),
    (2,"I would like to earn my first bachelor's degree and also become certified to teach."),
    (3,"I would like to apply to the Master of Education program."),
    (4,"I would like to apply to the Accelerated Certification for Teachers program."),
    (5,"I already have a bachelor's degree and now would like to earn certification to teach."),
)

PROGRAM_CHOICES = (
    ("7week","7 week format"),
    ("14week","14 week Undergraduate or Graduate"),
)

# 7 week years
if MONTH > 8:
    YEAR7 =+ 1

# 14 week years
if MONTH > 2 and MONTH < 10:
    YEAR14 =+ 1

SESSION7 = (
    ("7-AG-%s" % YEAR7, "January %s" % YEAR7),
    ("7-AK-%s" % YEAR7, "February %s" % YEAR7),
    ("7-AM-%s" % YEAR7, "April %s" % YEAR7),
    ("7-AS-%s" % YEAR7, "May %s" % YEAR7),
    ("7-AT-%s" % YEAR7, "July %s" % YEAR7),
)
SESSION14 = (
    ("14-A-%s" % YEAR14, "September %s" % YEAR14),
    ("14-C-%s" % YEAR14, "February %s" % YEAR14),
)

class ContactForm(forms.ModelForm):
    """
    Contact form based on the generic processor model
    """
    previous_last_name  = forms.CharField(max_length=128, required=False, label="Previous Last Name")
    phone               = USPhoneNumberField(max_length=12, help_text="Format: XXX-XXX-XXXX")
    state               = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=True)
    postal_code         = USZipCodeField(label="Zip")

    class Meta:
        model = Contact
        exclude = ('country',)

class PersonalForm(forms.Form):
    """
    personal data
    """
    gender              = forms.TypedChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    ss_num              = USSocialSecurityNumberField(label="Social security number")
    dob                 = forms.DateField(label = "Date of birth", help_text="Format: dd/mm/yyyy")
    pob                 = forms.CharField(label = "Place of birth", help_text="City, state, zip, country", max_length=255)

class EmploymentForm(forms.Form):
    """
    employment history
    """
    # current employment
    employer            = forms.CharField(max_length=128, required=False)
    position            = forms.CharField(max_length=128, required=False)
    tuition_reimburse   = forms.TypedChoiceField(choices=BINARY_CHOICES, widget=forms.RadioSelect(), label="Does your employer offer tuition reimbursement?")

class EducationGoalsForm(forms.Form):

    educationalgoal     = forms.TypedChoiceField(choices=EDUCATION_GOAL, widget=forms.RadioSelect(), label="What degree are you intending to pursue?")
    program             = forms.TypedChoiceField(choices=PROGRAM_CHOICES, widget=forms.RadioSelect(), label="Choose the scheduling format")
    session7            = forms.TypedChoiceField(choices=SESSION7, widget=forms.RadioSelect(), label="Upcoming 7 Week Sessions")
    session14           = forms.TypedChoiceField(choices=SESSION14, widget=forms.RadioSelect(), label="Upcoming 14 Week Sessions")
    intented_major      = forms.CharField(max_length=128)
    intented_minor      = forms.CharField(max_length=128)
    certificiation      = forms.CharField(max_length=128, label="Intended certification")

