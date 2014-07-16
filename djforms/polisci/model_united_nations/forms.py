# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.contrib.localflavor.us.forms import USZipCodeField

from djforms.polisci.model_united_nations.models import Attender
from djforms.polisci.model_united_nations.models import Country
from djforms.core.models import STATE_CHOICES, PAYMENT_CHOICES
from djforms.processors.models import Order

DELEGATIONS = (
    ('', '----'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)

COUNTRIES = Country.objects.filter(status=True).order_by("name")

class AttenderForm(forms.ModelForm):
    """
    A form to collect registration data for the Model United Nations
    """
    first_name = forms.CharField(
        max_length=128, label="Faculty advisor first name"
    )
    last_name = forms.CharField(
        max_length=128
    )
    city = forms.CharField(
        max_length=128,
        required=True
    )
    address = forms.CharField(
        max_length=128,
        required=True
    )
    state = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES), required=True
    )
    postal_code = USZipCodeField(label="Zip Code")
    phone = USPhoneNumberField(
        help_text="Format: XXX-XXX-XXXX"
    )
    number_of_del = forms.TypedChoiceField(
        choices=DELEGATIONS, label="Number of delegations"
    )
    comments = forms.CharField(
        label="Questions/Comments",
        help_text="""
            Feel free to list alternate countries in the space above
            (include your choice and delegation number)
        """,
        widget=forms.Textarea, required=False
    )

    class Meta:
        model = Attender
        exclude = (
            'country','order','second_name','previous_name','salutation',
            'delegation_1','delegation_2','delegation_3','delegation_4',
            'delegation_5'
        )

class CountryForm(forms.Form):
    """
    Delegation countries
    """
    delegation_1 = forms.ModelChoiceField(
        queryset=COUNTRIES,
        required=False
    )
    delegation_2 = forms.ModelChoiceField(
        queryset=COUNTRIES,
        required=False
    )
    delegation_3 = forms.ModelChoiceField(
        queryset=COUNTRIES,
        required=False
    )
    delegation_4 = forms.ModelChoiceField(
        queryset=COUNTRIES,
        required=False
    )
    delegation_5 = forms.ModelChoiceField(
        queryset=COUNTRIES,
        required=False
    )

    '''
    def clean(self):
        from collections import Counter
        mylist = [20, 30, 25, 20]
        [k for k,v in Counter(mylist).items() if v>1]
        # returns [20]
        for k,v in Counter(mylist).items():
            if v>1:
                print k
        # for python 2.6
        l = [1,2,3,4,4,5,5,6,1]
        list(set([x for x in l if l.count(x) > 1]))

    #https://stackoverflow.com/questions/9835762/find-and-list-duplicates-in-python-list
    def moooeeeep(l):
        seen = set()
        seen_add = seen.add
        # adds all elements it doesn't know yet to seen and all other to seen_twice
        seen_twice = set( x for x in l if x in seen or seen_add(x) )
        # turn the set into a list (as requested)
        return list( seen_twice )
    '''

class OrderForm(forms.ModelForm):
    """
    Payment choices and total
    """
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect()
    )
    total = forms.CharField(
        max_length=7,
        label="Registration Fee"
    )

    class Meta:
        model = Order
        fields = ('total',)