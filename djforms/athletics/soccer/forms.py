from django import forms
from djforms.core.models import GENDER_CHOICES, BINARY_CHOICES, PAYMENT_CHOICES
from djforms.core.models import STATE_CHOICES
from djforms.processors.models import Contact
from djforms.athletics.soccer.models import SoccerCampAttender, YEAR_CHOICES, REQ
from djforms.athletics.soccer.models import SHIRT_SIZES, SESSIONS, AMOUNT_CHOICES

from localflavor.us.forms import USPhoneNumberField, USZipCodeField

class SoccerCampInsuranceCardForm(forms.Form):

    first_name = forms.CharField(
        label="Camper's First Name",
        max_length=128,widget=forms.TextInput(attrs=REQ)
    )
    last_name = forms.CharField(
        label="Camper's Last Name", max_length=128,
        widget=forms.TextInput(attrs=REQ)
    )
    email = forms.CharField(
        max_length=75,widget=forms.TextInput(attrs=REQ)
    )
    insurance_card_front = forms.FileField(
        max_length="256"
    )
    insurance_card_back = forms.FileField(
        max_length="256"
    )


class SoccerCampRegistrationForm(forms.ModelForm):
    """
    A form to collect registration data for the summer soccer camp
    """
    # contact info
    first_name = forms.CharField(
        label="Camper's First Name",
        max_length=128,widget=forms.TextInput(attrs=REQ)
    )
    last_name = forms.CharField(
        label="Camper's Last Name", max_length=128,
        widget=forms.TextInput(attrs=REQ)
    )
    email = forms.CharField(
        max_length=75,widget=forms.TextInput(attrs=REQ)
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
        widget=forms.TextInput(attrs={
                'class': 'required input-small','maxlength':'10'
            }
        )
    )
    phone = USPhoneNumberField(
        widget=forms.TextInput(attrs=REQ)
    )
    # personal info
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect()
    )
    dob = forms.DateField(
        label = "Date of birth",
        help_text="Format: mm/dd/yyyy"
    )
    age = forms.CharField(
        max_length=2
    )
    years_attend = forms.TypedChoiceField(
        label="Number of years attended",
        choices=YEAR_CHOICES, widget=forms.RadioSelect(),
        help_text="Include this year"
    )
    goalkeeper = forms.ChoiceField(
        label="Goalkeeper?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect()
    )
    shirt_size = forms.CharField(
        label="T-shirt size",
        widget=forms.Select(choices=SHIRT_SIZES)
    )
    # contact info
    parent_guard = forms.CharField(
        label="Parent or guardian name",
        max_length=100
    )
    # housing
    roommate = forms.CharField(
        label="Roommate request",
        max_length=100, required=False,
        help_text="Only one roommate per room"
    )
    dorm = forms.CharField(
        label="Reside in dorm",
        max_length=100, required=False,
        help_text="""
            Near teammates and/or friends&mdash;please be specific
            (player's names &amp; team name)
        """
    )
    # session
    session = forms.TypedChoiceField(
        choices=SESSIONS, widget=forms.RadioSelect(),
        help_text="<strong>Note</strong>: enrollment is limited."
    )
    football = forms.ChoiceField(
        label="Soccer ball",
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
        help_text="""
            <strong>Resident campers</strong>, please check here if you
            would like to purchase an official camp soccer ball for
            $30.00. Payment for ball and deposit must accompany
            application.
        """
    )
    # payment
    reg_fee = forms.CharField(
        label="Registration Fee Total",
        max_length=7
    )
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect()
    )
    amount = forms.TypedChoiceField(
        choices=AMOUNT_CHOICES, widget=forms.RadioSelect(),
        help_text="NOTE: NO CREDIT CARDS ACCEPTED AT CHECK-INS"
    )

    class Meta:
        model = SoccerCampAttender
        exclude = (
            'country','order','second_name','previous_name','salutation',
            'medical_history','assumption_risk','insurance_card_front',
            'insurance_card_back'
        )

