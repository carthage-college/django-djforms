from django import forms
from django.forms import ModelForm

from djforms.catering.models import Event
from djforms.core.models import GenericChoice

from djforms.core.fields import KungfuTimeField
from tagging.models import Tag, TaggedItem

import datetime

try:
    building_tag    = Tag.objects.get(name__iexact='Building Name')
    BUILDINGS       = TaggedItem.objects.get_by_model(GenericChoice, building_tag).filter(active=True).order_by("name")
except:
    BUILDINGS       = GenericChoice.objects.none()

try:
    open_to_tag     = Tag.objects.get(name__iexact='Audience Choices')
    OPEN_TO         = TaggedItem.objects.get_by_model(GenericChoice, open_to_tag).filter(active=True).order_by("name")
except:
    OPEN_TO         = GenericChoice.objects.none()

try:
    room_setup_tag  = Tag.objects.get(name__iexact='Room setup')
    ROOM_SET_UP     = TaggedItem.objects.get_by_model(GenericChoice, room_setup_tag).filter(active=True).order_by("ranking")
except:
    ROOM_SET_UP     = GenericChoice.objects.none()

try:
    meal_service    = Tag.objects.get(name__iexact='Meal service')
    MEAL_SERVICE    = TaggedItem.objects.get_by_model(GenericChoice, meal_service).filter(active=True).order_by("name")
except:
    MEAL_SERVICE    = GenericChoice.objects.none()

try:
    bar_pay_tag     = Tag.objects.get(name__iexact='Bar payment')
    BAR_PAY         = TaggedItem.objects.get_by_model(GenericChoice, bar_pay_tag).filter(active=True).order_by("ranking")
except:
    BAR_PAY         = GenericChoice.objects.none()

try:
    beverage_tag    = Tag.objects.get(name__iexact='Beverage options')
    BEVERAGES       = TaggedItem.objects.get_by_model(GenericChoice, beverage_tag).filter(active=True).order_by("name")
except:
    BEVERAGES       = GenericChoice.objects.none()

class EventForm1(forms.ModelForm):
    event_start     = KungfuTimeField(label="Event starts at", help_text="(Format HH:MM am/pm)")
    event_end       = KungfuTimeField(label="Event Ends at", help_text="(Format HH:MM am/pm)")
    building        = forms.ModelChoiceField(queryset=BUILDINGS, label="Building name", help_text="Name of the building on campus")

    class Meta:
        model = Event
        fields = ('extension', 'event_name', 'event_date', 'event_start', 'event_end', 'building', 'room_number')

    def clean_event_date(self):
        # dates
        today = datetime.date.today()
        event_date = self.cleaned_data.get('event_date')
        biz_date = today

        # minimum of 3 business days prior. handles past and current days.
        for i in range(3):
            biz_date += datetime.timedelta(days=1)
            # monday = 0
            while biz_date.weekday() not in (0,1,2,3,4):
                biz_date += datetime.timedelta(days=1)
        if event_date < biz_date:
            raise forms.ValidationError("Minimum of 3 business days before event date.")

        # maximum of 180 days into the future
        if event_date >= (today + datetime.timedelta(days=180)):
            raise forms.ValidationError("Maximum of 180 days before event date.")
        return self.cleaned_data['event_date']

class EventForm2(forms.ModelForm):
    open_to         = forms.ModelMultipleChoiceField(queryset=OPEN_TO, widget=forms.CheckboxSelectMultiple(), required=True)

    class Meta:
        model = Event
        fields = ('department', 'coordinator', 'purpose', 'account_number', 'open_to', 'facility_att', 'housing_att')

class EventForm3(forms.ModelForm):
    room_set_up     = forms.ModelMultipleChoiceField(queryset=ROOM_SET_UP, widget=forms.CheckboxSelectMultiple(), label="Room set-up", help_text="Check all that apply", required=True)

    class Meta:
        model = Event
        fields = ('room_set_up', 'room_set_other', 'rounds', 'six_rect', 'table_cloth', 'breakout', 'registration', 'skirting', 'head', 'other_table')

class EventForm4(forms.ModelForm):
    service_start   = KungfuTimeField(label="Service time start", help_text="(format HH:MM am/pm)")
    service_end     = KungfuTimeField(label="Service time end", help_text="(format HH:MM am/pm)")
    program_start   = KungfuTimeField(label="Program time start", help_text="(format HH:MM am/pm)")
    program_end     = KungfuTimeField(label="Program time end", help_text="(format HH:MM am/pm)")
    meal_service    = forms.ModelChoiceField(queryset=MEAL_SERVICE)
    bar_payment     = forms.ModelChoiceField(queryset=BAR_PAY, widget=forms.RadioSelect(), empty_label=None, label="Bar payment options")
    beverages       = forms.ModelMultipleChoiceField(queryset=BEVERAGES, widget=forms.CheckboxSelectMultiple(), label="Beverage requirements", required=False)

    class Meta:
        model = Event
        fields = ('dining_att', 'service_start', 'service_end', 'program_start', 'program_end', 'meal_service', 'menu_desc', 'other_reqs', 'bar_payment', 'beverages')

class EventForm5(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('slide', 'data_proj', 'overhead', 'tv_dvd', 'cordless_mic', 'fixed_mic', 'flip_chart', 'coat_rack', 'chalkboard', 'laptop', 'table_podium', 'free_podium', 'screen', 'other_equip')
