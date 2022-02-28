# -*- coding: utf-8 -*-

from django import forms
from django.utils.safestring import mark_safe
from djforms.core.models import REQ
from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.wsgc.conference.models import Registration
from djforms.wsgc.conference.models import MEAL_CHOICES
from djforms.wsgc.conference.models import PAYMENT_CHOICES
from djforms.wsgc.conference.models import REGISTRATION_TYPES
from djtools.fields import BINARY_CHOICES
from djtools.fields import STATE_CHOICES
from djtools.fields.localflavor import USPhoneNumberField


class RegistrationForm(ContactForm):
    """
    WSGC conference registration contact form, extends
    base ContactForm in processors app
    """

    #address1 = forms.CharField(max_length=255,widget=forms.TextInput(attrs=REQ))
    #city = forms.CharField(max_length=128,widget=forms.TextInput(attrs=REQ))
    state = forms.CharField(
        help_text = 'Choose "Other" if outside the United States',
        widget=forms.Select(choices=STATE_CHOICES, attrs=REQ)
    )
    phone = USPhoneNumberField(help_text='Format: XXX-XXX-XXXX')
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(),
    )

    class Meta:
        model = Registration
        fields = (
            'title',
            'first_name',
            'last_name',
            'suffix',
            'full_name',
            'institution',
            'address1',
            'address2',
            'city',
            'state',
            'postal_code',
            'email',
            'phone',
            'registration_type',
            'dietary_restrictions',
            'change_policy',
            'payment_method',
        )


class RegistrationOrderForm(OrderForm):
    """Conference registration form, extends base OrderForm in processors app."""

    total = forms.CharField()

    class Meta:
        model = Order
        fields = ('total', 'avs', 'auth')
