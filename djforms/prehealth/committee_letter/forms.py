# -*- coding: utf-8 -*-
from django import forms

from djforms.prehealth.committee_letter.models import Applicant
from djforms.prehealth.committee_letter.models import PROGRAMS_CHOICES
from djforms.prehealth.committee_letter.models import Recommender

from djtools.fields import BINARY_CHOICES


class ApplicantForm(forms.ModelForm):

    programs_apply = forms.MultipleChoiceField(
        label = "What Programs are you applying for?",
        choices=PROGRAMS_CHOICES, widget=forms.CheckboxSelectMultiple()
    )
    first_generation = forms.TypedChoiceField(
        label = "Are you a first generation college student?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
    )

    class Meta:
        model = Applicant
        exclude = (
            'created_by','created_on','updated_by','updated_on'
        )


class RecommenderForm(forms.ModelForm):

    class Meta:
        model = Recommender
        exclude = ('user',)

    def clean_email(self):
        email = self.cleaned_data['email']
        return email
