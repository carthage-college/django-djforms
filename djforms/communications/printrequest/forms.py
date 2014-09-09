# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from localflavor.us.forms import USPhoneNumberField

from djforms.communications.printrequest.models import PrintRequest, FORMATS

class PrintRequestForm(forms.ModelForm):

    phone = USPhoneNumberField(
        label = "Phone number",
        max_length=12,
        required=True,
        widget=forms.TextInput(attrs={'class': 'required phoneUS'})
    )

    print_format = forms.MultipleChoiceField(
        label = "What is the format of your finished piece",
        choices=FORMATS,
        help_text="Check all that apply"
    )

    def clean(self):
        cleaned_data = super(PrintRequestForm, self).clean()
        is_mailing = cleaned_data.get("is_mailing")
        who_mailing = cleaned_data.get("who_mailing")
        how_mailing = cleaned_data.get("how_mailing")
        speed_mailing = cleaned_data.get("speed_mailing")

        if is_mailing == "Yes":
            msg = "Required"
            if who_mailing == "":
                self._errors["who_mailing"] = self.error_class(["Required field."])
            if how_mailing == "":
                self._errors["how_mailing"] = self.error_class(["Required field."])
            if speed_mailing == "":
                self._errors["speed_mailing"] = self.error_class(["Required field."])

        return cleaned_data

    class Meta:
        model = PrintRequest
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'eg. 123-456-7890', 'class': 'phoneUS'
            }),
        }
        exclude = (
            'user','updated_by','date_created','date_updated'
        )

