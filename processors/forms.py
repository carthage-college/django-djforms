from django import forms
from django.contrib.localflavor.us.forms import USZipCodeField

from djforms.core.models import STATE_CHOICES
from djforms.processors.models import GenericPayment
from djforms.processors.trust_commerce import PaymentProcessor

# dummy classes to hold data
class Contact(object):
    pass

class Card(object):
    pass

class Order(object):
    def __init__(self):
        self.contact = Contact()
        self.card = Card()

class GenericPaymentForm(forms.ModelForm):
    """
    A generic form to collect credit card information and the charge the credit card.
    """
    amount              = forms.CharField(max_length=100)
    cc_first_name       = forms.CharField(max_length=100, label="First name on credit card", required=False)
    cc_last_name        = forms.CharField(max_length=100, label="Last name on credit card", required=False)
    billing_address1    = forms.CharField(max_length=255, label="Billing address", required=False)
    billing_address2    = forms.CharField(max_length=255, label="", required=False)
    billing_city        = forms.CharField(max_length=128, required=False)
    billing_state       = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=False)
    billing_postal_code = USZipCodeField(label="Billing zip", required=False)
    card_number         = forms.CharField(max_length=19, required=False)
    expiration_month    = forms.CharField(max_length=2, required=False)
    expiration_year     = forms.CharField(max_length=4, required=False)
    security_code       = forms.CharField(max_length=4, required=False)

    class Meta:
        model = GenericPayment

class TrustCommerceForm(GenericPaymentForm):
    """
    Trust commerce payment processor
    """

    def __init__(self, amount=None, *args, **kwargs):
        """
        Allow transaction amount to be passed in for authorizing the credit card during
        validation.
        """
        self.amount = amount
        self.processor_response = None
        super(TrustCommerceForm, self).__init__(*args, **kwargs)

    def clean(self):
        """
        In addition to validating form fields, attempt to process the payment
        and update form fields on errors from processor.
        """
        super(TrustCommerceForm, self).clean()
        cleaned_data = self.cleaned_data
        if not self.is_valid():
            return cleaned_data

        card = CreditCard(
            number = cleaned_data.get('card_number'),
            month = cleaned_data.get('expiration_month'),
            year = cleaned_data.get('expiration_year'),
            first_name = cleaned_data.get('cc_first_name'),
            last_name = cleaned_data.get('cc_last_name'),
            code = cleaned_data.get('security_code')
        )

        response = PaymentProcessor(order)
        if response.status != response.APPROVED:
            raise forms.ValidationError("%s %s" % (response.status_strings[response.status], response.message))

        self.processor_response = response

        return cleaned_data
