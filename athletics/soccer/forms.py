from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from quix.pay.transaction import CreditCard
from quix.pay.gateway import gateway_factory

from djforms.core.models import GENDER_CHOICES, STATE_CHOICES, BINARY_CHOICES

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
    ('Girls resident|395', 'Girls Resident $395.00'),
    ('Girls commuter|295', 'Girls Commuter $295.00'),
    ('Boys & Girls Jr. Kickers|100', 'Boys & Girls Jr. Kickers $100.00'),
    ('Boys resident|395', 'Boys Resident $395.00'),
    ('Boys commuter|295', 'Boys Commuter $295.00'),
    ('Boys & Girls day camp|195', 'Boys & Girls Day $195.00'),
    ('Boys & Girls Jr. Kickers|100', 'Boys & Girls. Jr. Kickers $100.00'),
    ('Soccer mom camp|245', 'Soccer Mom Camp $245'),
)

PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Check', 'Check'),
    ('Cash/Money Order ', 'Cash/Money Order '),
)

AMOUNT_CHOICES = (
    ('Deposit', 'Deposit'),
    ('Full amount', 'Full amount'),
)

class SoccerCampRegistrationForm(forms.Form):
    """
    A form to collect credit card information and the charge the credit card
    using the Authorize.Net payment gateway.
    """
    # personal info
    gender              = forms.TypedChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect())
    first_name          = forms.CharField(max_length=100)
    last_name           = forms.CharField(max_length=100)
    address             = forms.CharField(max_length=255)
    city                = forms.CharField(max_length=128)
    state               = forms.CharField(widget=forms.Select(choices=STATE_CHOICES))
    postal_code         = USZipCodeField(label="Zip code")
    years_attend        = forms.TypedChoiceField(choices=YEAR_CHOICES, widget=forms.RadioSelect(), label="Past years attended")
    email               = forms.EmailField()
    dob                 = forms.DateField(label = "Date of birth")
    goalkeeper          = forms.ChoiceField(choices=BINARY_CHOICES, widget=forms.RadioSelect(), label="Goalkeeper?")
    shirt_size          = forms.CharField(widget=forms.Select(choices=SHIRT_SIZES), label="T-shirt size")
    # contact info
    parent_guard        = forms.CharField(max_length=100, label="Parent or guardian name")
    home_phone          = USPhoneNumberField(max_length=12, required=False)
    work_phone          = USPhoneNumberField(max_length=12, required=False)
    # housing
    roommate            = forms.CharField(max_length=100, label="Roommate request", required=False)
    dorm                = forms.CharField(max_length=100, label="Reside in dorm", help_text="Near teammates and/or friends&mdash;please be specific", required=False)
    # session
    session             = forms.TypedChoiceField(choices=SESSIONS, widget=forms.RadioSelect(), help_text="<strong>Note</strong>: enrollment is limited.</p>")
    football            = forms.ChoiceField(choices=BINARY_CHOICES, widget=forms.RadioSelect(), label="", help_text="<strong>Resident campers</strong>, please check here if you would like to purchase an official camp soccer ball for $25.00. Payment for ball and deposit must accompany application.")
    # payment
    reg_fee             = forms.CharField(max_length=7, label="Registration Fee Total")
    payment_method      = forms.TypedChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect())
    amount              = forms.TypedChoiceField(choices=AMOUNT_CHOICES, widget=forms.RadioSelect())
    # ecommerce
    cc_first_name       = forms.CharField(max_length=100, label="First name on credit card")
    cc_last_name        = forms.CharField(max_length=100, label="Last name on credit card")
    billing_address1    = forms.CharField(max_length=255, label="Billing address")
    billing_address2    = forms.CharField(max_length=255, label="", required=False)
    billing_city        = forms.CharField(max_length=128)
    billing_state       = forms.CharField(widget=forms.Select(choices=STATE_CHOICES))
    billing_postal_code = USZipCodeField(label="Billing zip")
    card_number         = forms.CharField(max_length=19)
    expiration_month    = forms.CharField(max_length=2)
    expiration_year     = forms.CharField(max_length=4)
    security_code       = forms.CharField(max_length=4)

    def __init__(self, amount=None, *args, **kwargs):
        """
        Allow sale amount to be passed in for authorizing the credit card during
        validation.
        """
        self.amount = amount
        self.gateway_response = None
        super(SoccerCampRegistrationForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        In addition to validating form fields, attempt to process the payment
        and update form fields on errors from Authorize.Net.
        """
        super(SoccerCampRegistrationForm, self).clean()
        cleaned_data = self.cleaned_data
        if not self.is_valid():
            return cleaned_data

        if not hasattr(settings, 'GATEWAY_API_LOGIN'):
            raise ImproperlyConfigured("You need to specify GATEWAY_API_LOGIN in your Django settings file.")
        if not hasattr(settings, 'GATEWAY_TRANS_KEY'):
            raise ImproperlyConfigured("You need to specify GATEWAY_TRANS_KEY in your Django settings file.")
        if not self.amount:
            raise ValueError("An amount must be specified to process the payment.")

        # use the gateway factory for support of multiple gateways
        gateway_name = getattr(settings, 'GATEWAY_NAME', 'AimGateway')
        gateway = gateway_factory(gateway_name)
        gateway.authentication(settings.GATEWAY_API_LOGIN, settings.GATEWAY_TRANS_KEY)
        gateway.use_test_mode = getattr(settings, 'GATEWAY_USE_TEST_MODE', True)
        gateway.use_test_url = getattr(settings, 'GATEWAY_USE_TEST_URL', True)

        card = CreditCard(
            number = cleaned_data.get('card_number'),
            month = cleaned_data.get('expiration_month'),
            year = cleaned_data.get('expiration_year'),
            first_name = cleaned_data.get('cc_first_name'),
            last_name = cleaned_data.get('cc_last_name'),
            code = cleaned_data.get('security_code')
        )

        if getattr(settings, 'GATEWAY_AUTHORIZE_ONLY', True):
            response = gateway.authorize(self.amount, card)
        else:
            response = gateway.sale(self.amount, card)
        if response.status != response.APPROVED:
            raise forms.ValidationError("%s %s" % (response.status_strings[response.status], response.message))

        self.gateway_response = response

        return cleaned_data
