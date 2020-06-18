import datetime

from django import forms
from django.conf import settings
from djforms.processors.models import Contact
from djforms.processors.forms import OrderForm
from djforms.processors.models import Order
from djforms.athletics.soccer.models import AMOUNT_CHOICES
from djforms.athletics.soccer.models import REQ
from djforms.athletics.soccer.models import SoccerCampAttender
from djforms.athletics.soccer.models import SESSIONS
from djforms.athletics.soccer.models import SHIRT_SIZES
from djforms.athletics.soccer.models import YEAR_CHOICES

from djtools.fields import BINARY_CHOICES
from djtools.fields import GENDER_CHOICES
from djtools.fields import PAYMENT_CHOICES
from djtools.fields import STATE_CHOICES
from djtools.fields import TODAY
from djtools.fields.localflavor import USPhoneNumberField

from localflavor.us.forms import USZipCodeField


class SoccerCampInsuranceCardForm(forms.Form):
    """Upload of insurance card images."""

    first_name = forms.CharField(
        label="Camper's First Name",
        max_length=128,
        widget=forms.TextInput(attrs=REQ),
    )
    last_name = forms.CharField(
        label="Camper's Last Name",
        max_length=128,
        widget=forms.TextInput(attrs=REQ),
    )
    email = forms.CharField(
        max_length=75,
        widget=forms.TextInput(attrs=REQ),
    )
    insurance_card_front = forms.FileField(max_length=256)
    insurance_card_back = forms.FileField(max_length=256)


class SoccerCampBalanceForm(forms.ModelForm):
    """A form to collect registration data for the summer soccer camp."""

    first_name = forms.CharField(
        label="Your first name",
        required=True,
    )
    last_name = forms.CharField(
        label="Your last name",
        required=True,
    )
    email = forms.EmailField(
        label="Your email",
        required=True,
    )

    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email')


class SoccerCampBalanceOrderForm(OrderForm):
    """Credit card proceessor order form."""

    total = forms.CharField(label="Balance to pay")

    class Meta:
        model = Order
        fields = (
            'total', 'comments', 'avs', 'auth',
        )


class SoccerCampRegistrationForm(forms.ModelForm):
    """A form to collect registration data for the summer soccer camp."""

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
            'country',
            'order',
            'second_name',
            'previous_name',
            'salutation',
            'medical_history',
            'assumption_risk',
            'insurance_card_front',
            'insurance_card_back',
            'address2',
        )
