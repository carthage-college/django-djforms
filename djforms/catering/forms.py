from django import forms
from django.forms import ModelForm

from djforms.catering.models import Event
from djforms.core.models import GenericChoice

from djtools.fields.time import KungfuTimeField

import datetime

BUILDINGS = GenericChoice.objects.filter(
    tags__name__in=['Building Name']
).filter(active=True).order_by('name')

OPEN_TO = GenericChoice.objects.filter(
    tags__name__in=['Audience Choices']
).filter(active=True).order_by('name')

ROOM_SET_UP = GenericChoice.objects.filter(
    tags__name__in=['Room setup']
).filter(active=True).order_by('name')

MEAL_SERVICE = GenericChoice.objects.filter(
    tags__name__in=['Meal service']
).filter(active=True).order_by('name')


class EventForm1(forms.ModelForm):
    event_start = KungfuTimeField(
        label="Event starts at", help_text="(Format HH:MM am/pm)"
    )
    event_end = KungfuTimeField(
        label="Event Ends at", help_text="(Format HH:MM am/pm)"
    )
    building = forms.ModelChoiceField(
        label="Building name", queryset=BUILDINGS,
        help_text="Name of the building on campus"
    )

    class Meta:
        model = Event
        fields = (
            'extension', 'event_name', 'event_date', 'event_start',
            'event_end', 'building', 'room_number'
        )

    def clean_event_date(self):
        # dates
        today = datetime.date.today()
        event_date = self.cleaned_data.get('event_date')
        biz_date = today

        # minimum of 3 business days prior. handles past and current days.
        '''
        for i in range(3):
            biz_date += datetime.timedelta(days=1)
            # monday = 0
            while biz_date.weekday() not in (0,1,2,3,4):
                biz_date += datetime.timedelta(days=1)
        if event_date < biz_date:
            raise forms.ValidationError(
                """
                Minimum of 3 business days before event date.
                """
            )
        '''

        # maximum of 180 days into the future
        if event_date >= (today + datetime.timedelta(days=180)):
            raise forms.ValidationError(
                """
                Maximum of 180 days before event date.
                """
            )
        return self.cleaned_data['event_date']


class EventForm2(forms.ModelForm):
    open_to = forms.ModelMultipleChoiceField(
        queryset=OPEN_TO, widget=forms.CheckboxSelectMultiple(), required=True
    )

    class Meta:
        model = Event
        fields = (
            'department', 'coordinator', 'purpose', 'account_number',
            'open_to', 'facility_att', 'housing_att'
        )


class EventForm3(forms.ModelForm):
    room_set_up = forms.ModelMultipleChoiceField(
        label="Room set-up",
        queryset=ROOM_SET_UP, widget=forms.CheckboxSelectMultiple(),
        help_text="Check all that apply", required=True
    )

    class Meta:
        model = Event
        fields = (
            'room_set_up', 'room_set_other', 'rounds', 'six_rect',
            'table_cloth', 'breakout', 'registration', 'skirting',
            'head', 'other_table'
        )


class EventForm4(forms.ModelForm):
    service_start = KungfuTimeField(
        label="Service time start", help_text="(format HH:MM am/pm)"
    )
    service_end = KungfuTimeField(
        label="Service time end", help_text="(format HH:MM am/pm)"
    )
    program_start = KungfuTimeField(
        label="Program time start", help_text="(format HH:MM am/pm)"
    )
    program_end = KungfuTimeField(
        label="Program time end", help_text="(format HH:MM am/pm)"
    )
    meal_service = forms.ModelChoiceField(queryset=MEAL_SERVICE)

    class Meta:
        model = Event
        fields = (
            'dining_att', 'service_start', 'service_end', 'program_start',
            'program_end', 'meal_service', 'menu_desc', 'other_reqs'
        )


class EventForm5(forms.ModelForm):

    class Meta:
        model = Event
        fields = (
            'slide', 'data_proj', 'overhead', 'tv_dvd', 'cordless_mic',
            'fixed_mic', 'flip_chart', 'coat_rack', 'chalkboard', 'laptop',
            'table_podium', 'free_podium', 'screen', 'other_equip'
        )

