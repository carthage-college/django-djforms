from django import forms
from django.utils.safestring import mark_safe

from djforms.core.models import REQ
from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.polisci.iea.registration.models import RegistrationContact
from djforms.polisci.iea.registration.models import PAYMENT_CHOICES, REGGIES
from djforms.polisci.iea.registration.models import SERVE_AS_CHOICES

from djtools.fields import BINARY_CHOICES
from djtools.fields import STATE_CHOICES

from django_countries.widgets import CountrySelectWidget


class RegistrationContactForm(ContactForm):
    """
    IEA conference registration contact form, extends
    base ContactForm in processors app
    """

    def __init__(self, *args, **kwargs):
        # globally override the Django >=1.6 default of ':'
        kwargs.setdefault('label_suffix', '')
        super(RegistrationContactForm, self).__init__(*args, **kwargs)

    address1 = forms.CharField(
        max_length=255,widget=forms.TextInput(attrs=REQ)
    )
    city = forms.CharField(
        max_length=128,widget=forms.TextInput(attrs=REQ)
    )
    state = forms.CharField(
        help_text = 'Choose "Other" if outside the United States',
        widget=forms.Select(choices=STATE_CHOICES, attrs=REQ)
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs=REQ)
    )
    serve_as = forms.TypedChoiceField(
        label=mark_safe("Do you wish to serve as a&#133;?"),
        choices=SERVE_AS_CHOICES, widget=forms.RadioSelect(),
        help_text='''
            If so, please provide your Discipline and Specialty below.
        ''',
        required=False
    )
    registration_fee = forms.TypedChoiceField(
        choices=REGGIES, widget=forms.RadioSelect(),
        help_text="""
            All fees are stated in US Dollars
        """
    )
    kao_member = forms.TypedChoiceField(
        label = "Do you have KAO membership?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
        help_text = """
            KAO Members receive a $50 discount on the Registration Fee.
        """
    )
    abstract = forms.TypedChoiceField(
        label = "Did you submit an abstract and pay the $50 fee?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
        help_text = """
            Registrants who submitted an abstract and paid the fee receive a
            $50 discount on the Registration Fee.
        """
    )
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect(),
        help_text = '''
            NOTE: There is a 3% service charge added to the registration fee
            for credit card transactions.
        '''
    )

    class Meta:
        model = RegistrationContact
        fields = (
            'first_name','last_name','institution','email',
            'address1','address2','city','state','postal_code','country',
            'phone','serve_as','discipline','specialty','registration_fee',
            'kao_member','abstract','payment_method'
        )
        widgets = {'country': CountrySelectWidget}


class RegistrationOrderForm(OrderForm):
    """
    Conference registration order form, extends
    base OrderForm in processors app
    """
    total = forms.CharField()

    class Meta:
        model       = Order
        fields      = ('total','avs','auth')

