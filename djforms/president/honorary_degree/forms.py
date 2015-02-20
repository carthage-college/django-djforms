# -*- coding: utf-8 -*-
from django import forms

from djforms.president.honorary_degree.models import Nomination

from captcha.fields import CaptchaField


class NominationForm(forms.ModelForm):

    candidate_class_year = forms.CharField(
        label="Candidate class year (if applicable)",
        required=False
    )
    cv = forms.FileField(
        label="CV or résumé", max_length="256"
    )
    first_name = forms.CharField(label="Your first name")
    last_name = forms.CharField(label="Your last name")
    class_year = forms.CharField(
        label="Your class year (if applicable)",
        required=False
    )
    email = forms.EmailField()
    captcha = CaptchaField(
        label = """
            Input the text you see in the image on the left
        """,
        required=True
    )

    class Meta:
        model = Nomination
        fields = (
            'candidate_first_name','candidate_last_name',
            'candidate_class_year', 'reason','links','cv','first_name',
            'last_name','email','class_year','captcha'
        )

