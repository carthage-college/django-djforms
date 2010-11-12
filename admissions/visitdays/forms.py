from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from djforms.admissions.visitdays.models import VisitDayBaseProfile, VisitDayProfile, VisitDayEvent
from djforms.core.models import STATE_CHOICES

from tagging.models import TaggedItem

import datetime

now = datetime.datetime.today()

class VisitDayBaseForm(forms.ModelForm):

    date = forms.ChoiceField(choices=())
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    address = forms.CharField(label="Street Address")
    city = forms.CharField()
    state = forms.CharField(widget=forms.Select(choices=STATE_CHOICES))
    postal_code = USZipCodeField(label="Zip Code")
    phone = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    mobile = USPhoneNumberField(required=False, help_text="Format: XXX-XXX-XXXX")
    number_attend = forms.CharField(label="Number Attending", widget=forms.Select(choices=[('','--'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]))

    class Meta:
        model = VisitDayBaseProfile

    def __init__(self,event_type,*args,**kwargs):
        super(VisitDayBaseForm,self).__init__(*args,**kwargs)
        qs = VisitDayEvent.objects.exclude(active=False).filter(date__gte=now).filter(event__slug=event_type)
        choices = [('','---choose a date---')]
        for event in qs:
            choices.append((event.id,event))
        self.fields['date'].choices = choices
        self.fields.keyOrder = ['date','number_attend','first_name','last_name','email','address','city','state','postal_code','phone','mobile','gender']

class VisitDayForm(forms.ModelForm):

    number_attend = forms.CharField(label="Number Attending", widget=forms.Select(choices=[('','--'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]))

    class Meta:
        model = VisitDayProfile

    def __init__(self,event_type,*args,**kwargs):
        super(VisitDayForm,self).__init__(*args,**kwargs)
        qs = VisitDayEvent.objects.exclude(active=False).filter(date__gte=now).filter(event__slug=event_type)
        choices = [('','---choose a date---')]
        for event in qs:
            choices.append((event.id,event))
        self.fields['date'].choices = choices
        self.fields.keyOrder = ['date','number_attend','first_name','last_name',
                                'email','address','city','state','postal_code',
                                'phone','mobile','gender','high_school','hs_city',
                                'hs_state','hs_grad_year','entry_as','transfer',
                                'entry_year','entry_term','academic','xtracurricular',
                                'comments']

    def clean_transfer(self):
        if self.cleaned_data.get('entry_as')=="Transfer" and not self.cleaned_data.get('transfer'):
            raise forms.ValidationError("If you are a transfer student, please list the school from which you are trasferring.")

class WeekdayForm(VisitDayForm):
    class Meta:
        model = VisitDayProfile

class SaturdayForm(VisitDayForm):
    class Meta:
        model = VisitDayProfile

class TransferForm(VisitDayForm):
    class Meta:
        model = VisitDayProfile
