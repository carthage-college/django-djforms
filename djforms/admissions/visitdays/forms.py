from django import forms
from djforms.admissions.visitdays.models import GUARDIAN_CHOICES
from djforms.admissions.visitdays.models import VisitDay
from djforms.admissions.visitdays.models import VisitDayBaseProfile
from djforms.admissions.visitdays.models import VisitDayEvent
from djforms.admissions.visitdays.models import VisitDayProfile
from djforms.core.models import GenericChoice
from djforms.core.models import STATE_CHOICES

from djtools.fields.localflavor import USPhoneNumberField
from djtools.fields import TODAY

from localflavor.us.forms import USZipCodeField


MEETING_REQUEST = GenericChoice.objects.filter(
    tags__name__in=['Meeting Requests']
).filter(active=True).order_by('name')


class VisitDayBaseForm(forms.ModelForm):

    email = forms.EmailField(label="Email")
    postal_code = USZipCodeField(label="Zip Code")
    phone = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    mobile = USPhoneNumberField(
        required=False, help_text="Format: XXX-XXX-XXXX",
    )
    number_attend = forms.IntegerField(
        label="Number Attending",
        required=False,
        widget=forms.Select(
            choices=[
                ('', '--'),
                ('1', '1'),
                ('2', '2'),
                ('3', '3'),
                ('4', '4'),
                ('5', '5'),
            ]
        ),
    )
    meeting_request = forms.ModelMultipleChoiceField(
        label="Meeting Requests",
        queryset=MEETING_REQUEST,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = VisitDayBaseProfile
        fields = [
            'date',
            'date_alternate',
            'time_primary',
            'time_secondary',
            'number_attend',
            'meeting_format',
            'meeting_request',
            'first_name',
            'last_name',
            'email',
            'address',
            'city',
            'state',
            'postal_code',
            'phone',
            'mobile',
            'gender',
        ]

    def __init__(self, event_type, *args, **kwargs):
        try:
            self.visit_day = VisitDay.objects.get(slug=event_type)
        except Exception:
            self.visit_day = None
        super(VisitDayBaseForm, self).__init__(*args, **kwargs)
        qs = VisitDayEvent.objects.exclude(active=False).filter(
            date__gte=TODAY,
        ).filter(event__slug=event_type).order_by('date', 'id')
        choices = [('', '---choose a date---')]
        for event in qs:
            choices.append((event.id, event))
        self.fields['date'].choices = choices
        self.fields['date_alternate'].choices = choices
        if self.visit_day and self.visit_day.time_slots:
            self.fields['time_primary'].widget.attrs['class'] = 'required'

    def clean_number_attend(self):
        attend = self.cleaned_data.get('number_attend', 0)
        if self.visit_day.number_attend and not attend:
            raise forms.ValidationError("""
                Please provide the number of attendees.
            """)
        if self.visit_day.number_attend and self.cleaned_data.get('date'):
            event = VisitDayEvent.objects.get(
                pk=self.cleaned_data.get('date').id,
            )
            if (event.cur_attendees + attend) > event.max_attendees:
                less = event.max_attendees - event.cur_attendees
                raise forms.ValidationError("""
                    Attendee limit reached: {} places remain.
                    Please call us to arrange for more space,
                    or reduce the number attending.
                """.format(less))
        return self.cleaned_data['number_attend']

    def clean_date_alternate(self):
        cd = self.cleaned_data
        if cd.get('date_alternate') == cd.get('date'):
            raise forms.ValidationError("""
                Your second choice date cannot be the same as your first choice.
            """)
        return self.cleaned_data['date_alternate']

    def clean_time_primary(self):
        time = self.cleaned_data.get('time_primary')
        if self.visit_day and self.visit_day.time_slots and not time:
            raise forms.ValidationError("Please choose a time slot")
        return time

    def clean_time_secondary(self):
        tp = self.cleaned_data.get('time_primary')
        ts = self.cleaned_data.get('time_secondary')
        if self.visit_day and self.visit_day.time_slots and ts and ts == tp:
            raise forms.ValidationError("""
                Second time choice should not be the same as the first
            """)
        return ts

    def clean_meeting_request(self):
        mr = self.cleaned_data['meeting_request']
        if self.visit_day.meeting_request and mr.count() == 0:
            raise forms.ValidationError("""
                Please choose at least one meeting request.
            """)
        return mr


class VisitDayForm(forms.ModelForm):

    email = forms.EmailField(label="Student Email")
    guardian_email = forms.EmailField(label="Parent Email", required=False)
    guardian_type = forms.ChoiceField(
        label="",
        widget=forms.RadioSelect,
        choices=GUARDIAN_CHOICES,
        required = False,
    )
    postal_code = USZipCodeField(
        label="Zip Code",
        help_text="Format: 99999 or 99999-9999",
    )
    phone = USPhoneNumberField(help_text="Format: XXX-XXX-XXXX")
    mobile = USPhoneNumberField(
        required=False,
        help_text="Format: XXX-XXX-XXXX",
    )
    number_attend = forms.CharField(
        label="Number Attending",
        widget=forms.Select(
            choices=[
                ('', '--'),
                ('1', '1'),
                ('2', '2'),
                ('3', '3'),
                ('4', '4'),
                ('5', '5'),
            ]
        ),
    )
    hs_grad_year = forms.CharField(max_length=4)
    entry_year = forms.CharField(max_length=4)
    meeting_request = forms.ModelMultipleChoiceField(
        label="Meeting Requests",
        queryset=MEETING_REQUEST,
        widget=forms.CheckboxSelectMultiple(),
        required=False,
    )

    class Meta:
        model = VisitDayProfile
        fields = [
            'date',
            'date_alternate',
            'time_primary',
            'time_secondary',
            'number_attend',
            'meeting_format',
            'meeting_request',
            'first_name',
            'last_name',
            'email',
            'guardian_email',
            'guardian_type',
            'address',
            'city',
            'state',
            'postal_code',
            'phone',
            'mobile',
            'gender',
            'high_school',
            'hs_city',
            'hs_state',
            'hs_grad_year',
            'entry_as',
            'transfer',
            'entry_year',
            'entry_term',
            'academic',
            'xtracurricular',
            'comments',
        ]

    def __init__(self, event_type, *args, **kwargs):
        try:
            self.visit_day = VisitDay.objects.get(slug=event_type)
        except Exception:
            self.visit_day = None
        super(VisitDayForm, self).__init__(*args, **kwargs)
        qs = VisitDayEvent.objects.exclude(active=False).filter(
            date__gte=TODAY,
        ).filter(event__slug=event_type).order_by('date', 'id')
        choices = [('','---choose a date---')]
        for event in qs:
            choices.append((event.id,event))
        self.fields['date'].choices = choices
        self.fields['date_alternate'].choices = choices
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
        if self.visit_day and self.visit_day.time_slots:
            self.fields['time_primary'].widget.attrs['class'] = 'required'

    def clean_date_alternate(self):
        cd = self.cleaned_data
        if cd.get('date_alternate') == cd.get('date'):
            raise forms.ValidationError("""
                Your second choice date cannot be the same as your first choice.
            """)
        return self.cleaned_data['date_alternate']

    def clean_transfer(self):
        cd = self.cleaned_data
        if cd.get('entry_as')=="Transfer" and not cd.get('transfer'):
            raise forms.ValidationError("""
                Please include the school you attended
                and the location (city & state).
            """)
        return self.cleaned_data['transfer']

    def clean_time_primary(self):
        time = self.cleaned_data.get('time_primary')
        if self.visit_day and self.visit_day.time_slots and not time:
            raise forms.ValidationError("Please choose a time slot")
        return time

    def clean_time_secondary(self):
        tp = self.cleaned_data.get('time_primary')
        ts = self.cleaned_data.get('time_secondary')
        if self.visit_day and self.visit_day.time_slots and ts and ts == tp:
            raise forms.ValidationError("""
                Second time choice should not be the same as the first
            """)
        return ts

    def clean_meeting_request(self):
        mr = self.cleaned_data['meeting_request']
        if self.visit_day.meeting_request and mr.count() == 0:
            raise forms.ValidationError("""
                Please choose at least one meeting request.
            """)
        return mr
