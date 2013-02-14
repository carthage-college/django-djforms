from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from djforms.core.models import GENDER_CHOICES, BINARY_CHOICES, PAYMENT_CHOICES

YEAR_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10 or more'),
)

SHIRT_SIZES = (
    ('', '---------'),
    ('Adult S', 'Adult S'),
    ('Adult M', 'Adult M'),
    ('Adult L', 'Adult L'),
    ('Adult XL', 'Adult XL'),
    ('Youth M', 'Youth M'),
    ('Youth L', 'Youth L'),
    ('Youth XL', 'Youth XL'),
)

SESSIONS = (
    ('Girls resident|445', 'Girls Resident $445.00 (Goalkeepers check here too--no additional fee)'),
    ('Girls commuter|295', 'Girls Commuter $295.00'),
    ('Boys & Girls Jr. Kickers Session I|100', 'Boys & Girls Jr. Kickers Session I $100.00'),
    ('Boys resident|445', 'Boys Resident $445.00 (Goalkeepers check here too--no additional fee)'),
    ('Boys commuter|295', 'Boys Commuter $295.00'),
    ('Boys & Girls day camp|195', 'Boys & Girls Day camp $195.00'),
    ('Boys & Girls Jr. Kickers Session II|100', 'Boys & Girls. Jr. Kickers Session II $100.00'),
    ('Soccer mom camp|245', 'Soccer Mom Camp $245'),
)

AMOUNT_CHOICES = (
    ('Deposit', 'Deposit'),
    ('Full amount', 'Full amount'),
)

class SoccerCampRegistrationForm(forms.Form):
    """
    A form to collect registration data for the summer soccer camp
    """
    # personal info
    gender              = forms.TypedChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    dob                 = forms.DateField(label = "Date of birth", help_text="Format: dd/mm/yyyy")
    age                 = forms.CharField(max_length=2)
    years_attend        = forms.TypedChoiceField(choices=YEAR_CHOICES, widget=forms.RadioSelect(), label="Number of years attended", help_text="Include this year")
    goalkeeper          = forms.ChoiceField(choices=BINARY_CHOICES, widget=forms.RadioSelect(), label="Goalkeeper?")
    shirt_size          = forms.CharField(widget=forms.Select(choices=SHIRT_SIZES), label="T-shirt size")
    # contact info
    parent_guard        = forms.CharField(max_length=100, label="Parent or guardian name")
    # housing
    roommate            = forms.CharField(max_length=100, label="Roommate request", help_text="Only one roommate per room", required=False)
    dorm                = forms.CharField(max_length=100, label="Reside in dorm", help_text="Near teammates and/or friends&mdash;please be specific (player's names &amp; team name)", required=False)
    # session
    session             = forms.TypedChoiceField(choices=SESSIONS, widget=forms.RadioSelect(), help_text="<strong>Note</strong>: enrollment is limited.</p>")
    football            = forms.ChoiceField(choices=BINARY_CHOICES, widget=forms.RadioSelect(), label="Soccer ball", help_text="<strong>Resident campers</strong>, please check here if you would like to purchase an official camp soccer ball for $30.00. Payment for ball and deposit must accompany application.")
    # payment
    reg_fee             = forms.CharField(max_length=7, label="Registration Fee Total")
    payment_method      = forms.TypedChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect())
    amount              = forms.TypedChoiceField(choices=AMOUNT_CHOICES, widget=forms.RadioSelect(),help_text="NOTE: NO CREDIT CARDS ACCEPTED AT CHECK-INS")
