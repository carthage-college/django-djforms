from django import forms
from django.db import models
from django.forms import ModelForm
from djforms.eventform.models import *
from tagging.models import Tag, TaggedItem
from djforms.widgets import DateTimeWidget

#Sets up and populates the many to many fields on the EventForm based on entries in Generic Choice and their tags
try:
    entering_as_tag = Tag.objects.get(name__iexact='entering as')
    ENTERING_AS = TaggedItem.objects.get_by_model(GenericChoice, entering_as_tag).filter(active = True)
except:
    ENTERING_AS = GenericChoice.objects.none()

try:
    grad_year_tag = Tag.objects.get(name__iexact='grad year')
    GRAD_YEAR = TaggedItem.objects.get_by_model(GenericChoice, grad_year_tag).filter(active = True)
except:
    GRAD_YEAR = GenericChoice.objects.none()

try:
    entry_year_tag = Tag.objects.get(name__iexact='entry year')
    ENTRY_YEAR = TaggedItem.objects.get_by_model(GenericChoice, entry_year_tag).filter(active = True)
except:
    ENTRY_YEAR = GenericChoice.objects.none()

try:
    entry_term_tag = Tag.objects.get(name__iexact='entry term')
    ENTRY_TERM = TaggedItem.objects.get_by_model(GenericChoice, entry_term_tag).filter(active = True)
except:
    ENTRY_TERM = GenericChoice.objects.none()


class VisitDayForm(forms.ModelForm):
    event           = forms.ModelChoiceField(queryset=Event.objects.all(), empty_label=None, widget=forms.RadioSelect())
    name            = forms.CharField(max_length=100)
    address         = forms.CharField(max_length=100)
    city            = forms.CharField(max_length=100)
    state           = forms.CharField(max_length=100)
    zip             = forms.CharField(max_length=100)
    sex             = forms.ChoiceField(widget=forms.RadioSelect())
    email           = forms.CharField(max_length=100)
    email2          = forms.CharField(max_length=100)
    high school     = forms.CharField(max_length=100)
    hs_city         = forms.CharField(max_length=100)
    grad_year       = forms.ModelChoiceField(queryset=GRAD_YEAR, empty_label=None, widget=forms.Select())
    entering_as     = forms.ModelChoiceField(queryset=ENTERING_AS, empty_label=None, widget=forms.RadioSelect())
    entering_year   = forms.ModelChoiceField(queryset=ENTRY_YEAR, empty_label=None, widget=forms.Select())
    entering_term   = forms.ModelChoiceField(queryset=ENTRY_TERM, empty_label=None, widget=forms.Select())
    academic_interests = forms.TextField()
    extracurricular_interests = forms.TextField()

    class Meta:
        model = AdmissionVisitRegistrant

