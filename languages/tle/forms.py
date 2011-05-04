from django import forms

from djforms.core.models import BINARY_CHOICES, GENDER_CHOICES, MARITAL_CHOICES, SEMESTER_CHOICES

import datetime
NOW = datetime.datetime.now()

YEAR= int(NOW.year)

DEGREE_CHOICES = (
    ('Degree Seeking', 'Degree Seeking'),
    ('Non-Degree Seeking', 'Non-Degree Seeking'),
)
ENTRY_YEAR_CHOICES = (
    (YEAR,YEAR),
    (YEAR+1,YEAR+1)
)
class BaseForm(forms.Form):
    first_name          = forms.CharField(max_length=50)
    middle_name         = forms.CharField(max_length=50, required=False)
    last_name           = forms.CharField(max_length=50)
    second_last_name    = forms.CharField(max_length=50, required=False)
    gender              = forms.TypedChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())

    address             = forms.CharField(max_length=255)
    city                = forms.CharField(max_length=128)
    state               = forms.CharField(max_length=128, label='State/Provence')
    country             = forms.CharField(max_length=128)
    postal_code         = forms.CharField(max_length=10, label = 'Postal code')
    phone               = forms.CharField(max_length=12, label ='Telephone number')
    email               = forms.EmailField()

    birth_city          = forms.CharField(max_length=128, label = 'City')
    birth_state         = forms.CharField(max_length=128, label = 'State/Provence')
    birth_country       = forms.CharField(max_length=128, label = 'Country')
    dob                 = forms.DateField(label = "Birth date")
    citizen             = forms.CharField(max_length=128, label = 'Country of citizenship')


class ApplicationForm(BaseForm):

    education           = forms.CharField(required=False, widget=forms.Textarea, help_text="Where, when, degrees/diplomas earned and in-progress.")
    english             = forms.CharField(required=False, widget=forms.Textarea, help_text="Courses taken and your grades for each.")
    past_experience     = forms.CharField(required=False, widget=forms.Textarea, help_text="Past experience abroad, or working in educational settings.")
    personal_interests  = forms.CharField(required=False, widget=forms.Textarea)
    goals_ambitions     = forms.CharField(required=False, widget=forms.Textarea, label="Professional goals and ambitions")
    justification       = forms.CharField(required=False, widget=forms.Textarea, label="Why Carthage?", help_text="Reasons for wishing to spend two years teaching your languague at Carthage.")

class MastersForm(BaseForm):

    marital_status      = forms.TypedChoiceField(required=False, choices=MARITAL_CHOICES, widget=forms.RadioSelect(), help_text="The following is for statistical purposes only and is not used in admissions decisions.")
    entry_semester      = forms.TypedChoiceField(choices=SEMESTER_CHOICES, widget=forms.RadioSelect())
    entry_year          = forms.TypedChoiceField(choices=ENTRY_YEAR_CHOICES, widget=forms.RadioSelect())
    degree              = forms.TypedChoiceField(choices=DEGREE_CHOICES, widget=forms.RadioSelect(), label="Are you")
    military            = forms.TypedChoiceField(choices=BINARY_CHOICES, widget=forms.RadioSelect(), label="Military Service", help_text= "Have you ever served in the military?")

