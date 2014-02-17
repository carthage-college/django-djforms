from django import forms

class DistinguishedTeachingAward(forms.Form):
    nominee     = forms.CharField(label="I nominate")
    content     = forms.CharField(label="for the Distinguished Teaching Award because", widget=forms.Textarea)
    name        = forms.CharField(label="Your name")
    email       = forms.EmailField(label="Your email")
