from django import forms
from djforms.admissions.visitdays.models import VisitDayBaseProfile
from djforms.admissions.visitdays.models import VisitDayEvent
from djforms.admissions.visitdays.models import VisitDayProfile
from djforms.core.models import STATE_CHOICES

from localflavor.us.forms import USPhoneNumberField, USZipCodeField

import datetime

now = datetime.datetime.today()


class VisitDayBaseForm(forms.ModelForm):

    email = forms.EmailField()
    postal_code = USZipCodeField(label="Zip Code")
    phone = USPhoneNumberField(
        help_text="Format: XXX-XXX-XXXX"
    )
    mobile = USPhoneNumberField(
        required=False, help_text="Format: XXX-XXX-XXXX"
    )
    number_attend = forms.CharField(
        label="Number Attending",
        widget=forms.Select(
            choices=[
                ('','--'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')
            ]
        )
    )

    class Meta:
        model = VisitDayBaseProfile
        fields = [
            'date','number_attend','first_name','last_name','email',
            'address','city','state','postal_code','phone','mobile','gender'
        ]

    def __init__(self,event_type,*args,**kwargs):
        super(VisitDayBaseForm,self).__init__(*args,**kwargs)
        qs = VisitDayEvent.objects.exclude(active=False).filter(
            date__gte=now
        ).filter(event__slug=event_type).order_by("date","id")
        choices = [('','---choose a date---')]
        for event in qs:
            choices.append((event.id,event))
        self.fields['date'].choices = choices

    def clean_number_attend(self):
        if self.cleaned_data.get('date'):
            event = VisitDayEvent.objects.get(
                pk=self.cleaned_data.get('date').id
            )
            attend = int(self.cleaned_data.get('number_attend'))
            if (event.cur_attendees + attend) > event.max_attendees:
                less = event.max_attendees - event.cur_attendees
                raise forms.ValidationError("""
                    Attendee limit reached: {} places remain.
                    Please call us to arrange for more space,
                    or reduce the number attending.
                """.format(less))
        return self.cleaned_data['number_attend']


class VisitDayForm(forms.ModelForm):

    email = forms.EmailField()
    postal_code = USZipCodeField(
        label="Zip Code", help_text="Format: 99999 or 99999-9999"
    )
    phone = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    mobile = USPhoneNumberField(
        required=False, help_text="Format: XXX-XXX-XXXX"
    )
    number_attend = forms.CharField(
        label="Number Attending",
        widget=forms.Select(
            choices=[
                ('','--'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5')
            ]
        )
    )
    hs_grad_year = forms.CharField(max_length=4)
    entry_year = forms.CharField(max_length=4)

    class Meta:
        model = VisitDayProfile
        fields = [
            'date','number_attend','first_name','last_name',
            'email','address','city','state','postal_code',
            'phone','mobile','gender','high_school','hs_city',
            'hs_state','hs_grad_year','entry_as','transfer',
            'entry_year','entry_term','academic','xtracurricular',
            'comments'
        ]

    def __init__(self,event_type,*args,**kwargs):
        super(VisitDayForm,self).__init__(*args,**kwargs)
        qs = VisitDayEvent.objects.exclude(active=False).filter(
            date__gt=now
        ).filter(event__slug=event_type).order_by("date", "id")
        choices = [('','---choose a date---')]
        for event in qs:
            choices.append((event.id,event))
        self.fields['date'].choices = choices
        self.fields['date'].widget.attrs['class'] = 'validate[required]'
        self.fields['number_attend'].widget.attrs['class'] = 'validate[required]'
        self.fields['first_name'].widget.attrs['class'] = 'validate[required]'
        self.fields['last_name'].widget.attrs['class'] = 'validate[required]'
        self.fields['email'].widget.attrs['class'] = 'validate[required,custom[email]]'
        self.fields['address'].widget.attrs['class'] = 'validate[required]'
        self.fields['city'].widget.attrs['class'] = 'validate[required,custom[onlyLetter]]'
        self.fields['state'].widget.attrs['class'] = 'validate[required]'
        self.fields['postal_code'].widget.attrs['class'] = 'validate[required,custom[zip]]'
        self.fields['phone'].widget.attrs['class'] = 'validate[required,custom[telephone]]'
        self.fields['gender'].widget.attrs['class'] = 'validate[required]'
        self.fields['high_school'].widget.attrs['class'] = 'validate[required]'
        self.fields['hs_city'].widget.attrs['class'] = 'validate[required]'
        self.fields['hs_state'].widget.attrs['class'] = 'validate[required]'
        self.fields['hs_grad_year'].widget.attrs['class'] = 'validate[required,custom[year]]'
        self.fields['entry_as'].widget.attrs['class'] = 'validate[required]'
        self.fields['transfer'].widget.attrs['class'] = 'validate[funcCall[ValidateTransfer]]'
        self.fields['entry_year'].widget.attrs['class'] = 'validate[required,custom[year]]'
        self.fields['entry_term'].widget.attrs['class'] = 'validate[required]'

    def clean_transfer(self):
        cd = self.cleaned_data
        if cd.get('entry_as')=="Transfer" and not cd.get('transfer'):
            raise forms.ValidationError("""
                Please include the school you attended
                and the location (city & state).
            """)
        return self.cleaned_data['transfer']

