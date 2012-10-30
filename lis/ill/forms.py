from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField

from djtools.fields.time import KungfuTimeField
from djforms.core.models import BINARY_CHOICES

import datetime

STATUS_CHOICES=[('', '---------- select ----------'),
                ('Undergraduate Student', 'Undergraduate Student'),
                ('Graduate Student', 'Graduate Student'),
                ('Faculty', 'Faculty'),
                ('College Staff', 'College Staff'),
                ('Library Staff', 'Library Staff'),]

class IllBaseForm(forms.Form):
    phone       = USPhoneNumberField()
    box_number  = forms.CharField(max_length="4", required=False)
    thesis      = forms.ChoiceField(choices=BINARY_CHOICES, widget=forms.RadioSelect(), help_text="Is this for your Senior or Master's Thesis?")
    status      = forms.ChoiceField(choices=STATUS_CHOICES)
    department  = forms.CharField(max_length=50)
    exp_date    = forms.DateField(label="Expiration Date", help_text="Date after which item is no longer needed.")

    #Makes sure the user picks a date later than today
    def clean_exp_date(self):
        return _clean_date(self.cleaned_data['exp_date'])

class BookRequestForm(IllBaseForm):
    # book info
    author      = forms.CharField(max_length=100, label="Author or Authors", help_text="If it is a collection, provide the editor or editors here.")
    title       = forms.CharField(max_length=200)
    publisher   = forms.CharField(max_length=100)
    pub_date    = forms.CharField(max_length=100, label="Publication date")
    isbn        = forms.CharField(max_length=17, required=False, label="ISBN")
    edition     = forms.CharField(max_length=17, required=False, label="Specific Edition?")
    source      = forms.CharField(max_length=255, help_text="Source of the request.", required=False)
    source2     = forms.CharField(max_length=255, required=False, label="Other Source")
    comments    = forms.CharField(widget=forms.Textarea, required=False)

class ArticleRequestForm(IllBaseForm):
    # article info
    journal     = forms.CharField(max_length=100, label="Journal Name")
    volume      = forms.CharField(max_length=100, label="Volume")
    number      = forms.CharField(max_length=100, label="Issue Number")
    pub_date    = forms.CharField(max_length=100, label="Publication date")
    pages       = forms.CharField(max_length=100)
    author      = forms.CharField(max_length=100, label="Author", help_text="Include only the first listed author of the article.")
    title       = forms.CharField(max_length=200)
    issn        = forms.CharField(max_length=17, required=False, label="ISSN")
    source      = forms.CharField(max_length=255, help_text="Source of the request.", required=False)
    comments    = forms.CharField(widget=forms.Textarea, required=False)

class EricRequestForm(IllBaseForm):
    # ERIC info
    ericn       = forms.CharField(max_length=17, required=False, label="ERIC Document Number (ED#)")
    author      = forms.CharField(max_length=100, label="Author of document")
    title       = forms.CharField(max_length=200)
    pub_date    = forms.CharField(max_length=100, label="Publication date")
    comments    = forms.CharField(widget=forms.Textarea, required=False)

def _clean_date(date):
    if date <= datetime.date.today():
        raise forms.ValidationError("You must pick a date after today.")
    return date
