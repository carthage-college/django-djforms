from django import forms
from django.forms import ModelForm

from djforms.sustainability.green.models import Pledge

class PledgeForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Pledge
