from django import forms

class ContactForm(forms.Form):
    name        = forms.CharField(required=False)
    email       = forms.EmailField()
    comments    = forms.CharField(widget=forms.Textarea)
