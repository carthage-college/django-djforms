from django import forms
from django.conf import settings

from djforms.communications.printrequest.models import PrintRequest

class PrintRequestForm(forms.ModelForm):

    class Meta:
        model = PrintRequest
        exclude = ('file1','file2','file3','file4')
