from django import forms
from djforms.eduform.models import EduProfile
from djforms.eduform.models import GenericChoice
from tagging.models import Tag, TaggedItem

#Sets up and populates the many to many fields on the EduProfileForm based on entries in Generic Choice and their tags
PROGRAMS_OF_INTEREST = []
try:
    program_tag = Tag.objects.get(name='Programs Of Interest')
    programs = TaggedItem.objects.get_by_model(GenericChoice, program_tag)
    for p in programs.filter(active = True):
        PROGRAMS_OF_INTEREST.append((p.id,p.value))
except:
    pass

CONTACT_TIME = []
try:
    time_tag = Tag.objects.get(name='Contact Time')
    times = TaggedItem.objects.get_by_model(GenericChoice, time_tag)
    for t in times.filter(active = True):
        CONTACT_TIME.append((t.id,t.value))
except:
    pass

HOW_DID_YOU_HEAR_ABOUT_US = []
try:
    how_tag = Tag.objects.get(name='How Did You Hear About Us')
    hows = TaggedItem.objects.get_by_model(GenericChoice, how_tag)
    for h in hows.filter(active = True):
        HOW_DID_YOU_HEAR_ABOUT_US.append((h.id,h.value))
except:
    pass

class EduProfileForm(forms.ModelForm):
    programs_of_interest = forms.MultipleChoiceField(choices=PROGRAMS_OF_INTEREST, widget=forms.CheckboxSelectMultiple())
    contact_time = forms.ChoiceField(choices=CONTACT_TIME, widget=forms.RadioSelect())
    how_did_you_hear_about_us = forms.ChoiceField(choices=HOW_DID_YOU_HEAR_ABOUT_US, widget=forms.RadioSelect())
    
    class Meta:
        model = EduProfile

    def clean_programs_of_interest(self):
        if len(self.cleaned_data['programs_of_interest']) < 1:
            raise forms.ValidationError('Select at least one Program of Interest.')
        return self.cleaned_data['programs_of_interest']
    
    def clean_contact_time(self):
        if len(self.cleaned_data['contact_time']) < 1:
            raise forms.ValidationError('Select a Contact Time.')
        return self.cleaned_data['contact_time']
    
    def clean_how_did_you_hear_about_us(self):
        if len(self.cleaned_data['how_did_you_hear_about_us']) < 1:
            raise forms.ValidationError('Please tell us how you heard about us.')
        return self.cleaned_data['how_did_you_hear_about_us']