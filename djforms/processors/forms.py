from django import forms

from djforms.core.models import STATE_CHOICES
from models import Contact, Order
from trust_commerce import PaymentProcessor

from localflavor.us.forms import USPhoneNumberField, USZipCodeField

from datetime import date

EXP_MONTH = [(x, x) for x in xrange(1, 13)]
EXP_YEAR = [(x, x) for x in xrange(date.today().year, date.today().year + 15)]
REQ = {'class': 'required'}

class ContactForm(forms.ModelForm):
    """
    A generic form to collect contact info
    """
    phone = USPhoneNumberField(
        label="Phone number", max_length=12,
        help_text="Format: XXX-XXX-XXXX", required=False
    )
    state = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES), required=False
    )
    postal_code = USZipCodeField(required=False)

    class Meta:
        model = Contact
        exclude = (
            'country','order','second_name','previous_name',
            'salutation','longitude','latitude'
        )

class OrderForm(forms.ModelForm):
    """
    A generic form to collect order info
    """
    avs = forms.CharField(
        required = False,
        widget=forms.HiddenInput()
    )
    auth = forms.CharField(
        required = False,
        widget=forms.HiddenInput()
    )
    cycle = forms.CharField(
        required = False,
        widget=forms.HiddenInput()
    )
    total = forms.CharField(max_length=100)

    class Meta:
        model = Order
        fields = ('total',)

class CreditCardForm(forms.Form):
    """
    A generic form to collect credit card information
    and then charge the credit card.
    """
    def __init__(self, *args, **kwargs):
        # globally override the Django >=1.6 default of ':'
        kwargs.setdefault('label_suffix', '')
        super(CreditCardForm, self).__init__(*args, **kwargs)

    billing_name = forms.CharField(
        max_length=128, label="Name on card", widget=forms.TextInput(attrs=REQ)
    )
    card_number = forms.CharField(
        label="Card number", max_length=16, widget=forms.TextInput(attrs=REQ)
    )
    expiration_month = forms.CharField(
        max_length=2,
        widget=forms.Select(
            choices=EXP_MONTH, attrs={'class': 'required input-mini'}
        )
    )
    expiration_year = forms.CharField(
        max_length=4,
        widget=forms.Select(
            choices=EXP_YEAR, attrs={'class': 'required input-small'}
        )
    )
    security_code = forms.CharField(
        max_length=4,
        help_text="""
            The three or four digit security code
            on the back of your credit card.
        """,
        widget=forms.TextInput(attrs=REQ)
    )


class TrustCommerceForm(CreditCardForm):
    """
    Trust commerce payment processor
    """

    def __init__(self, order=None, contact=None, *args, **kwargs):
        """
        Allow transaction amount to be passed in for authorizing
        the credit card during validation.
        """
        self.order = order
        self.contact = contact
        self.name = None
        self.card = None
        self.processor_response = None
        super(TrustCommerceForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        In addition to validating form fields, attempt to process the payment
        and update form fields on errors from processor.
        """
        super(TrustCommerceForm, self).clean()
        cleaned_data = self.cleaned_data
        self.card = cleaned_data.get("card_number")
        self.name = cleaned_data.get("billing_name")

        if not self.is_valid():
            return cleaned_data

        response  = PaymentProcessor(cleaned_data, self.order, self.contact)
        self.processor_response = response
        if response.status != "approved" and response.status != 'accepted':
            if response.msg == "cc":
                self._errors["card_number"] = self.error_class(
                    ["Invalid credit card number"]
                )
            elif response.msg == "cvv":
                self._errors["security_code"] = self.error_class(
                    ["Invalid security code"]
                )
            else:
                raise forms.ValidationError("Transaction was declined")
        '''
        if response.status == "decline":
            self._errors["card_number"] = self.error_class(
                ["Transaction was declined: {}".format(response.msg)]
            )
            raise forms.ValidationError(
                "Transaction was declined: {}".format(response.msg)
            )
        '''
        return cleaned_data
