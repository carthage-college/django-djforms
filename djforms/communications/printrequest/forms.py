from django import forms
from django.conf import settings

from djforms.communications.printrequest.models import PrintRequest

class PrintRequestForm(forms.ModelForm):

    reg_fee             = forms.CharField(max_length=7, label="Registration Fee Total")
    
    class Meta:
        model = PrintRequest
        exclude = ('file1','file2','file3','file4')
