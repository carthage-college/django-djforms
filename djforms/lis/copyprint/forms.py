# -*- coding: utf-8 -*-
from django import forms

from djforms.lis.copyprint.models import CardRequest, STATUS

class CardRequestForm(forms.ModelForm):

    status = forms.TypedChoiceField(
        label="What type of card are you requesting?",
        choices=STATUS,widget=forms.RadioSelect()
    )

    class Meta:
        model = CardRequest
        fields = '__all__'
