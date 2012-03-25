from django import forms
from django.forms import ModelForm

from djforms.dining.models import Event
from djforms.core.models import GenericChoice

from sputnik.apps.utilities.forms.fields import KungfuTimeField
from tagging.models import Tag, TaggedItem

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
    BAR_PAY         = TaggedItem.objects.get_by_model(GenericChoice, bar_pay_tag).filter(active=True).order_by("name")
except:
    BAR_PAY         = GenericChoice.objects.none()

try:
    beverage_tag    = Tag.objects.get(name__iexact='Beverage options')
    BEVERAGES       = TaggedItem.objects.get_by_model(GenericChoice, beverage_tag).filter(active=True).order_by("name")
except:
    BEVERAGES       = GenericChoice.objects.none()

class EventForm(forms.ModelForm):
    email           = forms.EmailField()
    building        = forms.ModelChoiceField(queryset=BUILDINGS, label="Building name", help_text="Name of the building on campus")
    open_to         = forms.ModelMultipleChoiceField(queryset=OPEN_TO, widget=forms.CheckboxSelectMultiple())
    room_set_up     = forms.ModelMultipleChoiceField(queryset=ROOM_SET_UP, widget=forms.CheckboxSelectMultiple(), label="Room set-up", help_text="Check all that apply")
    event_start     = KungfuTimeField(label="Event starts at", help_text="(Format HH:MM am/pm)")
    event_end       = KungfuTimeField(label="Event Ends at", help_text="(Format HH:MM am/pm)")
    service_start   = KungfuTimeField(label="Service time start", help_text="(format HH:MM am/pm)")
    service_end     = KungfuTimeField(label="Service time end", help_text="(format HH:MM am/pm)")
    program_start   = KungfuTimeField(label="Program time start", help_text="(format HH:MM am/pm)")
    program_end     = KungfuTimeField(label="Program time end", help_text="(format HH:MM am/pm)")
    meal_service    = forms.ModelChoiceField(queryset=MEAL_SERVICE)
    bar_payment     = forms.ModelMultipleChoiceField(queryset=BAR_PAY, widget=forms.CheckboxSelectMultiple(), label="Bar payment options")
    beverages       = forms.ModelMultipleChoiceField(queryset=BEVERAGES, widget=forms.CheckboxSelectMultiple(), label="Beverage requirements")

    class Meta:
        model = Event
        exclude = ('created_on','updated_on',)

