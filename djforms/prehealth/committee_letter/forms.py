# -*- coding: utf-8 -*-
from django import forms

from djforms.core.models import STATE_CHOICES
from djforms.core.models import GenericChoice
from djforms.prehealth.committee_letter.models import Applicant, Evaluation
from djforms.prehealth.committee_letter.models import RANKING_CHOICES
from djforms.prehealth.committee_letter.models import Recommendation

from djtools.fields import BINARY_CHOICES

from localflavor.us.forms import USPhoneNumberField

PROGRAM_CHOICES = GenericChoice.objects.filter(
    tags__name__in=['Pre-Health Programs']
).filter(active=True).order_by('name')


class ApplicantForm(forms.ModelForm):

    city = forms.CharField()
    state = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES)
    )
    phone = USPhoneNumberField()

    programs_apply = forms.ModelMultipleChoiceField(
        label = "For which programs are you applying?",
        widget=forms.CheckboxSelectMultiple(),
        queryset=PROGRAM_CHOICES, required=True
    )
    first_generation = forms.TypedChoiceField(
        label = "Are you a first generation college student?",
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
    )

    class Meta:
        model = Applicant
        fields = (
            'city','state','phone','programs_apply','first_generation',
            'graduation_date','major','minor','gpa_overall','gpa_bcpm',
            'mcat_dat_scores','mcat_dat_date','cv','personal_statements',
            'transcripts','waiver'
        )
        exclude = (
            'created_by','created_on','updated_by','updated_on'
        )


class EvaluationForm(forms.ModelForm):

    knowledge = forms.TypedChoiceField(
        label = "Knowledge of Subject Matter",
        choices=RANKING_CHOICES, widget=forms.RadioSelect(),
    )
    curiosity = forms.TypedChoiceField(
        label = "Intellectual Curiosity",
        choices=RANKING_CHOICES, widget=forms.RadioSelect(),
    )
    communication = forms.TypedChoiceField(
        label = "Communication Skills – Oral/Written",
        choices=RANKING_CHOICES, widget=forms.RadioSelect(),
    )
    cooperation = forms.TypedChoiceField(
        label = "Ability to get along with Others – Willingness to Cooperate",
        choices=RANKING_CHOICES, widget=forms.RadioSelect(),
    )
    maturity = forms.TypedChoiceField(
        label = "Maturity",
        choices=RANKING_CHOICES, widget=forms.RadioSelect(),
    )
    integrity = forms.TypedChoiceField(
        label = "Integrity",
        choices=RANKING_CHOICES, widget=forms.RadioSelect(),
    )
    overall = forms.TypedChoiceField(
        label = "Overall Evaluation",
        choices=RANKING_CHOICES, widget=forms.RadioSelect(),
    )

    class Meta:
        model = Evaluation
        exclude = ('applicant','created_by','updated_by')
