from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from djforms.core.models import STATE_CHOICES
from djforms.alumni.homecoming.models import Attendee

import datetime

GUESTS  = [(x, x) for x in xrange(0, 12)]
GUESTS.insert(0,("","---"))
YEARS   = [(x, x) for x in reversed(xrange(1926,datetime.date.today().year +1))]
YEARS.insert(0,("","---"))

class AttendeeForm(forms.ModelForm):
    email           = forms.EmailField(required=False)
    state           = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=False)
    grad_class      = forms.CharField(max_length=4, widget=forms.Select(choices=YEARS))
    guests          = forms.CharField(widget=forms.Select(choices=GUESTS))

    class Meta:
        model = Attendee
        exclude = ('created_on','updated_on',)

    def __init__(self,*args,**kwargs):
        super(AttendeeForm,self).__init__(*args,**kwargs)
        self.fields.keyOrder = ['first_name','last_name','maiden_name',
                                'email','city','state','grad_class','guests']
