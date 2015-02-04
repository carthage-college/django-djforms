# -*- coding: utf-8 -*-
from django import forms

from djforms.music.theatre.summer_camp.models import SummerCampAttender
from djforms.music.theatre.summer_camp.models import HOW_HEAR, PAYMENT_CHOICES
from djforms.music.theatre.summer_camp.models import VOICE_TYPE

from djtools.fields import BINARY_CHOICES, GENDER_CHOICES

class RegistrationForm(forms.ModelForm):
    last_name = forms.CharField(
        label="Last name (姓)"
    )
    first_name = forms.CharField(
        label="First name (名)"
    )
    dob = forms.DateField(
        label="Birthday (出生日)",
        help_text="(MM/DD/YYYY) (月月／日日／年年年年)"
    )
    gender = forms.TypedChoiceField(
        choices=GENDER_CHOICES,widget=forms.RadioSelect()
    )
    address = forms.CharField(
        label='Home address (家庭地址)',
        max_length=255,widget=forms.TextInput()
    )
    city = forms.CharField(
        label='City (城市)',max_length=128,
        widget=forms.TextInput()
    )
    postal_code = forms.CharField(
        label='Postal code (邮政编码)', max_length='6'
    )
    country = forms.CharField(
        label='Country (国家)',max_length=128
    )
    email = forms.EmailField(
        label='Email address (电子邮件信箱)'
    )
    phone = forms.CharField(
        label='Telephone number (电话)',max_length=18
    )
    voice_type = forms.TypedChoiceField(
        label="Entering level",choices=VOICE_TYPE,
        widget=forms.RadioSelect()
    )
    how_hear = forms.MultipleChoiceField(
        label="How did you hear about our Summer Camp in Music Theatre?",
        choices=HOW_HEAR,widget=forms.RadioSelect()
    )
    payment_method = forms.TypedChoiceField(
        choices=PAYMENT_CHOICES, widget=forms.RadioSelect()
    )

    class Meta:
        model = SummerCampAttender
        exclude = (
            'country','order','second_name','previous_name','salutation',
            'medical_history','assumption_risk','insurance_card_front',
            'insurance_card_back'
        )

