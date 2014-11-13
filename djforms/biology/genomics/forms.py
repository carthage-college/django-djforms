from django import forms

from djforms.core.models import STATE_CHOICES, BINARY_CHOICES
from djforms.biology.genomics.models import PhageHunter

from localflavor.us.forms import USPhoneNumberField, USZipCodeField

class PhageHunterForm(forms.ModelForm):
    email = forms.EmailField()
    postal_code = USZipCodeField(label="Zip Code")
    phone = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    lab_work = forms.CharField(
        widget=forms.RadioSelect(choices=BINARY_CHOICES),
        help_text="Are you willing to spend extra time in the lab as needed?"
    )

    class Meta:
        model = PhageHunter
        exclude = ('created_at','updated_at',)

    def clean(self):
        if not self.cleaned_data.get('act_comp') and not self.cleaned_data.get('act_math') and not self.cleaned_data.get('act_science') and not self.cleaned_data.get('sat_comp') and not self.cleaned_data.get('sat_math') and not self.cleaned_data.get('sat_read'):
            self._errors["act_comp"] = self.error_class(["Provide either ACT or SAT scores or both."])
            self._errors["act_math"] = self.error_class(["Provide either ACT or SAT scores or both."])
            self._errors["act_science"] = self.error_class(["Provide either ACT or SAT scores or both."])
            self._errors["sat_comp"] = self.error_class(["Provide either ACT or SAT scores or both."])
            self._errors["sat_math"] = self.error_class(["Provide either ACT or SAT scores or both."])
            self._errors["sat_read"] = self.error_class(["Provide either ACT or SAT scores or both."])
        return self.cleaned_data
