from django import forms
from djforms.eduform.models import *
from tagging.models import Tag, TaggedItem

#Sets up and populates the many to many fields on the EduProfileForm based on entries in Generic Choice and their tags
ACADEMIC_PROGRAMS = []
try:
    program_tag = Tag.objects.get(name='Academic Programs')
    ACADEMIC_PROGRAMS = TaggedItem.objects.get_by_model(GenericChoice, program_tag).filter(active = True)
except:
    pass

CONTACT_TIME = []
try:
    time_tag = Tag.objects.get(name='Contact Time')
    CONTACT_TIME = TaggedItem.objects.get_by_model(GenericChoice, time_tag).filter(active = True)
except:
    pass

HOW_DID_YOU_HEAR_ABOUT_US = []
try:
    how_tag = Tag.objects.get(name='How Did You Hear About Us')
    HOW_DID_YOU_HEAR_ABOUT_US = TaggedItem.objects.get_by_model(GenericChoice, how_tag).filter(active = True)
except:
    pass

class EduProfileForm(forms.ModelForm):
    academic_programs = forms.ModelMultipleChoiceField(queryset=ACADEMIC_PROGRAMS, widget=forms.CheckboxSelectMultiple())
    contact_time = forms.ModelChoiceField(queryset=CONTACT_TIME, empty_label=None, widget=forms.RadioSelect())
    how_did_you_hear_about_us = forms.ModelChoiceField(queryset=HOW_DID_YOU_HEAR_ABOUT_US, empty_label=None, widget=forms.Select())
    
    class Meta:
        model = EduProfile

    def clean_academic_programs(self):
        if len(self.cleaned_data['academic_programs']) < 1:
            raise forms.ValidationError('Please select at least one Academic Program.')
        return self.cleaned_data['academic_programs']
