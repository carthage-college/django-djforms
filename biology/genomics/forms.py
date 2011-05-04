from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from djforms.core.models import GENDER_CHOICES, STATE_CHOICES, BINARY_CHOICES
from djforms.biology.genomics.models import PhageHunter

MAJOR_CHOICES = (
    ('Biological Chemistry', 'Biologicial Chemistry'),
    ('Biology', 'Biology'),
    ('Mathematics', 'Mathematics'),
)

class PhageHunterForm(forms.ModelForm):
    email           = forms.EmailField()
    postal_code     = USZipCodeField(label="Zip Code")
    phone           = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    gender          = forms.CharField(widget=forms.RadioSelect(choices=GENDER_CHOICES))
    lab_work        = forms.CharField(widget=forms.RadioSelect(choices=BINARY_CHOICES), help_text="Are you willing to spend extra time in the lab as needed?")
    intended_majors = forms.MultipleChoiceField(required=False, choices=MAJOR_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = PhageHunter
        exclude = ('created_on','updated_on',)

    def clean(self):
        if not self.cleaned_data.get('intended_majors') and not self.cleaned_data.get('intended_majors_other'):
            self._errors["intended_majors"] = self.error_class(["Either check one or more boxes under 'Intended majors' or complete the 'Other' field."])
            del self.cleaned_data["intended_majors"]
            del self.cleaned_data["intended_majors_other"]
        return self.cleaned_data
