from django import forms
from django.db import models
from django.forms import ModelForm
from djforms.jobpost.models import JobApplyForm, Post
from tagging.models import Tag, TaggedItem
from djforms.widgets import DateTimeWidget

class JobApplyForm(forms.ModelForm):
    job         = forms.ModelChoiceField(Post, required=False, widget=forms.HiddenInput())
    class Meta:
        model = JobApplyForm
        
class Post(forms.ModelForm):
    publish     = forms.DateTimeField(help_text="A date for the post to go live on", widget=DateTimeWidget)
    expire_date = forms.DateTimeField(help_text="A date for the post to expire on", widget=DateTimeWidget)
    
    class Meta:
        model = Post
        
    #Makes sure the user picks an expire date later than the post date
    def clean_date(self):
        postdate = self.cleaned_data['publish']
        expiredate = self.cleaned_data['expire_date']
        if postdate >= expiredate:
            raise forms.ValidationError("You must pick an expire date later than the post date!")
        return expiredate