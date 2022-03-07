# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from djforms.scholars.models import Presentation
from djforms.core.models import BINARY_CHOICES
from djforms.core.models import Department


DEPTS = Department.objects.filter(tags__name__in=['WAC']).order_by('name')


class PresentationForm(forms.ModelForm):
    """Form class for the presentation form."""

    permission = forms.ChoiceField(
        label="Permission to reproduce",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        help_text="Do you grant Carthage permission to reproduce your presentation?",
    )
    shared = forms.ChoiceField(
        label="Faculty sponsor approval",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
        help_text="""
            Has your faculty sponsor approved your proposal?
            Note: Faculty and staff presenters should choose 'yes'.
        """,
    )
    need_table = forms.ChoiceField(
        label="Do you need a table for display purposes?",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )
    need_electricity = forms.ChoiceField(
        label="Do you need electricity for computer or other device?",
        choices=BINARY_CHOICES,
        widget=forms.RadioSelect(),
    )

    class Meta:
        """Sub-class for settings configurations about the parent class."""

        model = Presentation
        exclude = (
            'user',
            'reviewer',
            'updated_by',
            'date_created',
            'date_updated',
            'presenters',
            'ranking',
            'leader',
            'status',
            'work_type_other',
        )

    def __init__(self,*args,**kwargs):
        """Initialization method."""
        super(PresentationForm,self).__init__(*args,**kwargs)
        try:
            self.obj = Presentation.objects.get(pk=self.instance.pk)
        except Exception:
            self.obj = None
        self.fields.keyOrder = [
            'title',
            'funding',
            'work_type',
            'permission',
            'shared',
            'abstract_text',
            'need_table',
            'need_electricity',
            'poster_file',
        ]


class EmailPresentersForm(forms.Form):
    """Form class for the form to send emails to presenters."""

    content = forms.CharField(widget=forms.Textarea, label="Email content")
