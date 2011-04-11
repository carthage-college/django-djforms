from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from djforms.alumni.msw.models import ReunionContact

class ReunionContactForm(forms.ModelForm):
    email = forms.EmailField()
    postal_code = USZipCodeField(label="Zip Code")
    phone = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")

    class Meta:
        model = ReunionContact
        exclude = ('created_on','updated_on',)

    def clean_update(self):
        if len(self.cleaned_data.get('update')) > 500:
            raise forms.ValidationError("500 Character Max.")
        return self.cleaned_data.get('update')

