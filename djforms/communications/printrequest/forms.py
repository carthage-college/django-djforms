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
        
        if is_mailing is True:
            if who_mailing is None or how_mailing is None or speed_mailing is None:
                msg = "Required"
                self.add_error('who_mailing', msg)
                self.add_error('how_mailing', msg)
                self.add_error('speed_mailing', msg)
    
    class Meta:
        model = PrintRequest
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'eg. 123-456-7890'}),
            'delivery_date': forms.TextInput(attrs={'placeholder': 'eg. MM/DD/YYYY'})
        }
