from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from djforms.alumni.memory.models import Questionnaire

class QuestionnaireForm(forms.ModelForm):
    phone = USPhoneNumberField()
    postal_code = USZipCodeField()

    class Meta:
        model = Questionnaire
        exclude = ('photos',)
