# -*- coding: utf-8 -*-

from captcha.fields import CaptchaField
from django import forms
from djforms.security.models import ParkingTicketAppeal
from djforms.core.models import GenericChoice
from djforms.core.models import STATE_CHOICES
from djforms.core.models import BINARY_CHOICES


RESIDENCY_STATUS = GenericChoice.objects.filter(
    tags__name__in=['Residency Status'],
).filter(active=True).order_by('name')
PERMIT_TYPE = GenericChoice.objects.filter(
    tags__name__in=['Permit Type'],
).filter(active=True).order_by('name')


class ParkingTicketAppealForm(forms.ModelForm):
    """Form class for the parking ticket appeal form."""

    state = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES),
        required=True,
    )
    residency_status = forms.ModelChoiceField(
        queryset=RESIDENCY_STATUS,
        empty_label=None,
        widget=forms.RadioSelect(),
    )
    permit_type = forms.ModelChoiceField(
        queryset=PERMIT_TYPE,
        widget=forms.Select(),
        empty_label='Select Permit',
    )
    towed = forms.ChoiceField(
        label="Was your vehicle Towed?",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )

    class Meta:
        """Sub-class to set configurations about the parent class."""

        model = ParkingTicketAppeal
        exclude = ('created_at','updated_at')


class AnonymousReportForm(forms.Form):
    """Form that allows folks to submit a report anonymously."""

    report = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()

    class Meta:
        """Sub-class to set configurations about the parent class."""

        fields = ('report', 'captcha')
