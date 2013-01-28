from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from djforms.core.models import STATE_CHOICES
from models import Contact, Order
from trust_commerce import PaymentProcessor

from datetime import date

EXP_MONTH = [(x, x) for x in xrange(1, 13)]
EXP_YEAR = [(x, x) for x in xrange(date.today().year, date.today().year + 15)]

class ContactForm(forms.ModelForm):
    """
    A generic form to collect contact info
    """
    phone               = USPhoneNumberField(label="Phone number", max_length=12, help_text="Format: XXX-XXX-XXXX")
    state               = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=True)
    postal_code         = USZipCodeField()

    class Meta:
        model = Contact
        exclude = ('country','order','second_name','previous_name','salutation')

class OrderForm(forms.ModelForm):
    """
    A generic form to collect order info
    """
    avs                 = forms.CharField(widget=forms.HiddenInput())
    auth                = forms.CharField(widget=forms.HiddenInput())
    cycle               = forms.CharField(widget=forms.HiddenInput(), required=False)
    total               = forms.CharField(max_length=100, label="Donation")

    class Meta:
        model = Order
        fields = ('total',)

class CreditCardForm(forms.Form):
    """
    A generic form to collect credit card information and then charge the credit card.
    """
    billing_name        = forms.CharField(max_length=128, label="Name as it appears on credit card")
    card_number         = forms.CharField(max_length=19, help_text="xxxx-xxxx-xxxx-xxxx or xxxx-xxxx-xxxx-xxx")
    expiration_month    = forms.CharField(max_length=2, widget=forms.Select(choices=EXP_MONTH))
    expiration_year     = forms.CharField(max_length=4, widget=forms.Select(choices=EXP_YEAR))
    security_code       = forms.CharField(max_length=4, required=True, help_text="The three or four digit security code on the back of your credit card.")

from django.conf import settings

class TrustCommerceForm(CreditCardForm):
    """
    Trust commerce payment processor
    """

    def __init__(self, order=None, contact=None, *args, **kwargs):
        """
        Allow transaction amount to be passed in for authorizing the credit card during
        validation.
        """
        self.order = order
        self.contact = contact
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

        response = PaymentProcessor(cleaned_data, self.order, self.contact)
        self.processor_response = response
        if response.status != "approved" and response.status != 'accepted':
            if response.msg == "cc":
                self._errors["card_number"] = self.error_class(["Invalid credit card number"])
            elif response.msg == "cvv":
                self._errors["security_code"] = self.error_class(["Invalid security code"])
            else:
                raise forms.ValidationError("Transaction was declined")
        #if response.status == "decline":
            #self._errors["card_number"] = self.error_class(["Transaction was declined: %s" % response.msg])
        #    raise forms.ValidationError("Transaction was declined: %s" % response.msg)
        return cleaned_data
