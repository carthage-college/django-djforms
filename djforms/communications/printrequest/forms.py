from django import forms
from django.conf import settings

from djforms.communications.printrequest.models import PrintRequest

class PrintRequestForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(PrintRequestForm, self).clean()
        is_mailing = cleaned_data.get("is_mailing")
        who_mailing = cleaned_data.get("who_mailing")
        how_mailing = cleaned_data.get("how_mailing")
        speed_mailing = cleaned_data.get("speed_mailing")

        if is_mailing == "Yes":
            msg = "Required"
            if who_mailing == "":
                self._errors["who_mailing"] = self.error_class(["This is a required field."])
            if how_mailing == "":
                self._errors["how_mailing"] = self.error_class(["This is a required field."])
            if speed_mailing == "":
                self._errors["speed_mailing"] = self.error_class(["This is a required field."])

        return cleaned_data

    class Meta:
        model = PrintRequest
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            'delivery_date': forms.TextInput(attrs={'placeholder': 'eg. MM/DD/YYYY'})
        }
