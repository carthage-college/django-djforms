# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from djforms.core.models import REQ
from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.wsgc.conference.models import RegistrationContact
from djforms.wsgc.conference.models import PAYMENT_CHOICES, REGGIES
from djforms.wsgc.conference.models import REGGIES
from djtools.fields import BINARY_CHOICES
from djtools.fields import STATE_CHOICES
from django_countries.widgets import CountrySelectWidget


class RegistrationContactForm(ContactForm):
    """
    WSGC conference registration contact form, extends
    base ContactForm in processors app
    """

    address1 = forms.CharField(max_length=255,widget=forms.TextInput(attrs=REQ))
    city = forms.CharField(max_length=128,widget=forms.TextInput(attrs=REQ))
    state = forms.CharField(
        help_text = 'Choose "Other" if outside the United States',
        widget=forms.Select(choices=STATE_CHOICES, attrs=REQ)
    )
    phone = forms.CharField(widget=forms.TextInput(attrs=REQ))
    registration_fee = forms.TypedChoiceField(
        choices=REGGIES, widget=forms.RadioSelect(),
        help_text="""
            All fees are stated in US Dollars
        """
    )
    wsgc_member = forms.TypedChoiceField(
        label = "Do you have WSGC membership?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
        help_text = """
            WSGC Members receive a $50 discount on the Registration Fee.
        """
    )
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(),
    )

    class Meta:
        model = RegistrationContact
        fields = (
            'first_name',
            'last_name',
            'institution',
            'email',
            'address1',
            'address2',
            'city',
            'state',
            'postal_code',
            'country',
            'phone',
            'discipline',
            'specialty',
            'registration_fee',
            'wsgc_member',
            'payment_method',
        )
        widgets = {'country': CountrySelectWidget}


class RegistrationOrderForm(OrderForm):
    """Conference registration form, extends base OrderForm in processors app."""

    total = forms.CharField()

    class Meta:
        model = Order
        fields = ('total', 'avs', 'auth')
