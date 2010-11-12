from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from djforms.admissions.visitdays.models import VisitDayBaseProfile, VisitDayProfile, VisitDayEvent
from djforms.core.models import STATE_CHOICES

from tagging.models import TaggedItem

import datetime

now = datetime.datetime.today()

from django.conf import settings
import logging
logging.basicConfig(filename=settings.LOG_FILENAME,level=logging.DEBUG,)

class VisitDayBaseForm(forms.ModelForm):

    email = forms.EmailField()
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

    def clean_number_attend(self):
        if self.cleaned_data.get('date'):
            event = VisitDayEvent.objects.get(pk=self.cleaned_data.get('date').id)
            if (event.cur_attendees + int(self.cleaned_data.get('number_attend'))) > event.max_attendees:
                less = event.max_attendees - event.cur_attendees
                raise forms.ValidationError("Attendee limit reached: %s places remain. Please call us to arrange for more space, or reduce the number attending." % less)
        return self.cleaned_data['number_attend']

class VisitDayForm(forms.ModelForm):

    email = forms.EmailField()
    postal_code = USZipCodeField(label="Zip Code")
    phone = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    mobile = USPhoneNumberField(required=False, help_text="Format: XXX-XXX-XXXX")
    number_attend = forms.CharField(label="Number Attending", widget=forms.Select(choices=[('','--'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')]))

    class Meta:
        model = VisitDayProfile

    def __init__(self,event_type,*args,**kwargs):
        super(VisitDayForm,self).__init__(*args,**kwargs)
        qs = VisitDayEvent.objects.exclude(active=False).filter(date__gt=now).filter(event__slug=event_type)
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
        return self.cleaned_data['transfer']

class WeekdayForm(VisitDayForm):
    class Meta:
        model = VisitDayProfile

class SaturdayForm(VisitDayForm):
    class Meta:
        model = VisitDayProfile

class TransferForm(VisitDayForm):
    class Meta:
        model = VisitDayProfile