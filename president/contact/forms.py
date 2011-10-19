from django import forms

class ContactForm(forms.Form):
    name        = forms.CharField(label="Name (optional)", required=False)
    email       = forms.EmailField(label="Email (optional)", required=False)
    comments    = forms.CharField(widget=forms.Textarea)

