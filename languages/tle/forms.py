from django import forms

from djforms.widgets import *
from djforms.core.models import BINARY_CHOICES, GENDER_CHOICES


class BaseForm(forms.Form):
    first_name          = forms.CharField(max_length=50)
    middle_name         = forms.CharField(max_length=50, required=False)
    last_name           = forms.CharField(max_length=50)
    second_last_name    = forms.CharField(max_length=50)
    gender              = forms.CharField(max_length=16, choices=GENDER_CHOICES)

    address             = forms.CharField(max_length=255)
    city                = forms.CharField(max_length=128)
    state               = forms.CharField(max_length=128)
    country             = forms.CharField(max_length=128)
    postal_code         = models.CharField(max_length=10, label = 'Postal code')
    phone               = forms.CharField(max_length=12, label ='Telephone number')
    email               = forms.EmailField()

    birth_city          = forms.CharField(max_length=128, label = 'City')
    birth_state         = forms.CharField(max_length=128, label = 'State/Provence')
    birth_country       = forms.CharField(max_length=128, label = 'Country')
    dob                 = models.DateField(label = "Birth date")
    citizen             = forms.CharField(max_length=128, verbose_name = 'Country of citizenship')


class ApplicationForm(BaseForm):

class MastersForm(BaseForm):


