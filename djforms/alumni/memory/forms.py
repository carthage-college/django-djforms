from django import forms
from django.forms import ModelForm

from djforms.alumni.memory.models import Questionnaire

from localflavor.us.forms import USPhoneNumberField, USZipCodeField

class QuestionnaireForm(forms.ModelForm):
    phone = USPhoneNumberField()
    postal_code = USZipCodeField()

    class Meta:
        model = Questionnaire
        exclude = ('photos',)
