from django import forms

from djforms.communications.printrequest.models import *

class RequestForm(forms.ModelForm):
    
    class Meta:
        model = Request
 