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

class EventForm(forms.ModelForm):
    email           = forms.EmailField()
    building        = forms.ModelChoiceField(queryset=BUILDINGS)
    open_to         = forms.ModelMultipleChoiceField(queryset=OPEN_TO, widget=forms.CheckboxSelectMultiple())
    start_time      = KungfuTimeField()
    end_time        = KungfuTimeField()

    class Meta:
        model = Event
        exclude = ('created_on','updated_on',)

