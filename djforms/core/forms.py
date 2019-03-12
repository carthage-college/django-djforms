from django import forms
from django.forms import ModelForm
from djtools.fields.localflavor import USPhoneNumberField

from djforms.core.models import UserProfile


class UserProfileForm(forms.ModelForm):
    phone = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")

    class Meta:
        model = UserProfile
        exclude = ('user','creation_date','created_by','updated_by','state','permissions')

