# -*- coding: utf-8 -*-

from django import forms
from djforms.core.models import BINARY_CHOICES
from djtools.fields.localflavor import USPhoneNumberField


HOUSING_CHOICES = [
    ('', '---- select ----'),
    ('Family stay', 'Family stay'),
    ('Dormitory/Apt', 'Dormitory/Apt'),
]



class StudyAbroadForm(forms.Form):
    phone = USPhoneNumberField()
    campus_box = forms.CharField(required=False, max_length=4)
    majors = forms.CharField(required=False, max_length=50)
    minors = forms.CharField(required=False, max_length=50)
    parent_name = forms.CharField(max_length=50)
    parent_phone = USPhoneNumberField()
    parent_address = forms.CharField(widget=forms.Textarea)
    health_insurance = forms.CharField(
        max_length=50,
        help_text="Name of provider and type of provider (e.g. PPO, HMO)",
    )
    preferred_language = forms.CharField(
        max_length=10,
        label="Preferred Language of instruction while abroad",
    )
    recent_course = forms.CharField(
        label="Current or most recent language course taken at Carthage",
        max_length=50,
        help_text="(language, number, and term)",
    )
    desired_country = forms.CharField(
        widget=forms.Textarea,
        label="Country (or countries) under consideration",
    )
    school_program = forms.CharField(
        label="University/School Program abroad",
        help_text="(if known)",
        widget=forms.Textarea,
    )
    abroad_field = forms.CharField(
        label="Field of study while abroad",
        help_text="Specific coursework desired, if any",
        widget=forms.Textarea,
    )
    abroad_year = forms.CharField(
        label="Year/Term of anticipated Study Abroad",
        max_length=20,
    )
    current_year = forms.CharField(
        label="Current year in college",
        max_length=10,
    )
    previous_travel = forms.TypedChoiceField(
        label="Previous international travel or study abroad experience",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect,
    )
    traveled_places = forms.CharField(
        label="If yes, where?",
        max_length=100,
        required=False,
    )
    passport = forms.TypedChoiceField(
        label="Do you have a current passport?",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect,
    )
    passport_expiration = forms.CharField(
        label="Expiration Date",
        max_length=5,
        help_text="(mm/yy)",
        required=False,
    )
    housing = forms.ChoiceField(
        label="Preferred housing arrangements",
        choices=HOUSING_CHOICES,
        help_text="""
            Typically, we encourage our students to participate
            in the host family experience
        """,
    )

    def clean_traveled_places(self):
        """Verify previous countries travelled if they have traveled before."""
        traveled_places = self.cleaned_data.get('traveled_places')
        if self.cleaned_data.get('previous_travel') == 'Yes' and not traveled_places:
            raise forms.ValidationError(
                "Please enter previous countries that you have traveled to.",
            )
        return traveled_places

    def clean_passport_expiration(self):
        """Verify the user picks an end time after the start time."""
        passport_expiration = self.cleaned_data.get('passport_expiration')
        if self.cleaned_data.get('passport') == 'Yes' and not passport_expiration:
            raise forms.ValidationError("Please enter passport exiration date")
        return passport_expiration
