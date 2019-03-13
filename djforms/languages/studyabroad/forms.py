from django import forms

from djforms.core.models import BINARY_CHOICES

from djtools.fields.localflavor import USPhoneNumberField

HOUSING_CHOICES=[('', '---------- select ----------'),
                ('Family stay', 'Family stay'),
                ('Dormitory/Apt', 'Dormitory/Apt'),]


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
        help_text = "Name of provider and type of provider (e.g. PPO, HMO)"
    )
    preferred_language = forms.CharField(
        max_length=10, label="Preferred Language of instruction while abroad"
    )
    recent_course = forms.CharField(
        max_length=50,
        label="Current or most recent language course taken at Carthage",
        help_text="(language, number, and term)"
    )
    desired_country = forms.CharField(
        widget=forms.Textarea,
        label="Country (or countries) under consideration"
    )
    school_program = forms.CharField(
        label="University/School Program abroad",
        help_text="(if known)", widget=forms.Textarea
    )
    abroad_field = forms.CharField(
        label="Field of study while abroad",
        help_text="Specific coursework desired, if any", widget=forms.Textarea
    )
    abroad_year = forms.CharField(
        max_length=20, label="Year/Term of anticipated Study Abroad"
    )
    current_year = forms.CharField(
        max_length=10, label="Current year in college"
    )
    previous_travel = forms.TypedChoiceField(
        choices=BINARY_CHOICES, widget=forms.RadioSelect,
        label="Previous international travel or study abroad experience"
    )
    traveled_places = forms.CharField(
        max_length=100, label="If yes, where?", required=False
    )
    passport = forms.TypedChoiceField(
        choices=BINARY_CHOICES, widget=forms.RadioSelect,
        label="Do you have a current passport?"
    )
    passport_expiration = forms.CharField(
        max_length=5, label="Expiration Date",
        help_text="(mm/yy)", required=False
    )
    housing = forms.ChoiceField(
        choices=HOUSING_CHOICES,
        label="Preferred housing arrangements",
        help_text="""
            Typically, we encourage our students to participate
            in the host family experience
        """
    )

    # Makes sure the user enters previous countries
    # travelled if they have traveled before
    def clean_traveled_places(self):
        traveled_places = self.cleaned_data.get('traveled_places')
        if self.cleaned_data.get('previous_travel')=="Yes" and not traveled_places:
            raise forms.ValidationError(
                """
                Please enter previous countries that you have traveled to.
                """
            )
        return traveled_places

    #Makes sure the user picks an end time after the start time
    def clean_passport_expiration(self):
        passport_expiration = self.cleaned_data.get('passport_expiration')
        if self.cleaned_data.get('passport')=="Yes" and not passport_expiration:
            raise forms.ValidationError("Please enter passport exiration date")
        return passport_expiration

