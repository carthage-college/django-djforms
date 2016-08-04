# -*- coding: utf-8 -*-
from django import forms
from djforms.core.models import STATE_CHOICES
from djforms.core.models import BINARY_CHOICES
from djforms.polisci.mun import COUNTRIES

from localflavor.us.forms import USPhoneNumberField, USZipCodeField

DELEGATIONS = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

class AttenderForm(forms.Form):
    """
    A form to collect registration data for the Model United Nations
    """
    school_name = forms.CharField(
        max_length=100, label="School name"
    )
    first_name = forms.CharField(
        max_length=128, label="Faculty advisor first name"
    )
    last_name = forms.CharField(
        max_length=128
    )
    address1 = forms.CharField(
        max_length=128,
        label = "Address",
        required=True
    )
    address2 = forms.CharField(
        max_length=128,
        label = "",
        required=False
    )
    city = forms.CharField(
        max_length=128,
        required=True
    )
    state = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES), required=True
    )
    postal_code = USZipCodeField(label="Zip Code")
    office = forms.CharField(max_length=100)
    phone = USPhoneNumberField(
        help_text="Format: XXX-XXX-XXXX"
    )
    email = forms.EmailField()
    number_of_del = forms.TypedChoiceField(
        choices=DELEGATIONS, label="Number of delegations"
    )
    number_of_stu = forms.CharField(
        max_length=3, label="Number of students"
    )
    comments = forms.CharField(
        label="Questions/Comments",
        help_text="""
            Feel free to list alternate countries in the space above
            (include your choice and delegation number)
        """,
        widget=forms.Textarea, required=False
    )
    missle_crisis = forms.TypedChoiceField(
        label="""
            Do you want to be entered into the random draw for participation
            in the Historical Cuban Missile Crisis simulation?
        """,
        choices=BINARY_CHOICES, widget=forms.RadioSelect
    )

class CountryForm(forms.Form):
    # delegation 1
    d1c1  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d1c2  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d1c3  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d1c4  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d1c5  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    # delegation 2
    d2c1  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d2c2  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d2c3  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d2c4  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d2c5  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    # delegation 3
    d3c1  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d3c2  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d3c3  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d3c4  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d3c5  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    # delegation 4
    d4c1  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d4c2  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d4c3  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d4c4  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d4c5  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    # delegation 5
    d5c1  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d5c2  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d5c3  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d5c4  = forms.TypedChoiceField(choices=COUNTRIES, required=False)
    d5c5  = forms.TypedChoiceField(choices=COUNTRIES, required=False)

