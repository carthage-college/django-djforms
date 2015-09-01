# -*- coding: utf-8 -*-
from django import forms

from djforms.lis.copyprint.models import CardRequest, STATUS

class CardRequestForm(forms.ModelForm):

    status = forms.TypedChoiceField(
        choices=STATUS,widget=forms.RadioSelect()
    )

    class Meta:
        model = CardRequest
