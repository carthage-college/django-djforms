# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from djforms.core.models import UserProfile
from djtools.fields.localflavor import USPhoneNumberField


class UserProfileForm(forms.ModelForm):
    phone = USPhoneNumberField(help_text='Format: XXX-XXX-XXXX')

    class Meta:
        model = UserProfile
        exclude = (
            'user',
            'creation_date',
            'created_by',
            'updated_by',
            'state',
            'permissions',
        )
