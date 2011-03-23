from django import forms
from django.forms import ModelForm
from djforms.video.models import Contest

class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        exclude = ('user','updated_by','created_on','updated_on','tags',)
