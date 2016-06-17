# -*- coding: utf-8 -*-
from django import forms

from djforms.music.theatre.summer_camp.models import SummerCampAttender
from djforms.music.theatre.summer_camp.models import HOW_HEAR, PAYMENT_CHOICES
from djforms.music.theatre.summer_camp.models import VOICE_TYPE

from djtools.fields import BINARY_CHOICES, GENDER_CHOICES

from django_countries.widgets import CountrySelectWidget

class RegistrationForm(forms.ModelForm):
    last_name = forms.CharField(
        label="Last name (姓)"
    )
    first_name = forms.CharField(
        label="First name (名)"
    )
    address1 = forms.CharField(
        label='Home address (家庭地址)',
        max_length=255,widget=forms.TextInput()
    )
    city = forms.CharField(
        label='City (城市)',max_length=128,
        widget=forms.TextInput()
    )
    state = forms.CharField(
        label="Province",
        max_length=128
    )
    postal_code = forms.CharField(
        label='Postal code (邮政编码)', max_length='6'
    )
    email = forms.EmailField(
        label='Email address (电子邮件信箱)'
    )
    phone = forms.CharField(
        label='Telephone number (电话)',max_length=18,
        help_text="e.g. +86 xxx XXXX YYYY"
    )
    dob = forms.DateField(
        label="Birthday (出生日)",
        help_text="(MM/DD/YYYY) (月月／日日／年年年年)"
    )
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES,widget=forms.RadioSelect()
    )
    voice_type = forms.TypedChoiceField(
        choices=VOICE_TYPE,
        widget=forms.RadioSelect()
    )
    how_hear = forms.TypedChoiceField(
        label="How did you hear about our Summer Camp in Music Theatre?",
        choices=HOW_HEAR,widget=forms.RadioSelect()
    )
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect()
    )

    class Meta:
        model = SummerCampAttender
        exclude = (
            'order','second_name','previous_name','salutation','address2'
        )
        widgets = {'country': CountrySelectWidget}
