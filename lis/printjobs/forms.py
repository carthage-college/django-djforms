from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField
from djforms.widgets import *
from djforms.core.models import BINARY_CHOICES

PAPER_CHOICES = [
    ('Bond','Bond'),
    ('Cardstock', 'Cardstock'),
    ('Vellum', 'Vellum'),
]

class PrintRequestForm(forms.Form):
    name            = forms.CharField()
    department      = forms.CharField(max_length=50)
    email           = forms.EmailField()
    phone           = USPhoneNumberField(initial="262-551-", max_length=12)
    date_needed     = forms.DateField()
    originals       = forms.IntegerField(label="# of Originals", help_text="Each side counts as 1")
    copies          = forms.IntegerField(label="# of Copies")
    paper_type      = forms.ChoiceField(label="Type of Paper", choices=PAPER_CHOICES, widget=forms.RadioSelect())
    front_back      = forms.ChoiceField(label="Double Sided", choices=BINARY_CHOICES, widget=forms.RadioSelect())
    folded          = forms.ChoiceField(choices=BINARY_CHOICES, widget=forms.RadioSelect())
    stapled         = forms.ChoiceField(choices=BINARY_CHOICES, widget=forms.RadioSelect())
    collated        = forms.ChoiceField(choices=BINARY_CHOICES, help_text="(kept in order)", widget=forms.RadioSelect())
    cut             = forms.ChoiceField(label="Page content will be cut into pieces", choices=BINARY_CHOICES, widget=forms.RadioSelect())
    cut_number      = forms.IntegerField(label="If page content will be cut, number of pieces per page", required=False, help_text="(Paper is cut in Half, Thirds, Fourths, etc.)")
    instructions    = forms.CharField(label="Special Instructions", widget=forms.Textarea, required=False)

    #Makes certain that the user picks a date later than today
    def clean_date_needed(self):
        return _clean_date(self.cleaned_data['date_needed'])

    def clean_cut_number(self):
        if self.cleaned_data.get('cut')=="Yes" and not self.cleaned_data.get('cut_number'):
            raise forms.ValidationError("If you want the copies cut, you must included the number of pieces.")

def _clean_date(date):
    if date <= datetime.date.today():
        raise forms.ValidationError("You must pick a date after today.")
    return date
