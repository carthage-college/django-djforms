from django import forms

from djforms.communications.print.models import *

class RequestForm(forms.ModelForm):
    
    class Meta:
        model = Request
