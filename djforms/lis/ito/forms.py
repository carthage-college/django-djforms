from django import forms
from django.forms import ModelForm

from djforms.core.models import BINARY_CHOICES
from djforms.lis.ito.models import Profile

class ProfileForm(forms.ModelForm):
    partner     = forms.CharField(widget=forms.RadioSelect(choices=BINARY_CHOICES), help_text="Do you have a partner?")

    class Meta:
        model = Profile
        exclude = ('user','updated_by','created_on','updated_on',)

    def clean(self):
        if not self.cleaned_data.get('partner_name') and self.cleaned_data.get('partner')=="Yes":
            self._errors["partner_name"] = self.error_class(["If you have a partner, you must provide their name."])
        return self.cleaned_data
