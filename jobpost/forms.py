from django import forms
from django.db import models
from django.forms import ModelForm
from djforms.jobpost.models import JobApplyForm, Post
from tagging.models import Tag, TaggedItem
from djforms.widgets import DateTimeWidget

#Sets up and populates the many to many fields on the EduProfileForm based on entries in Generic Choice and their tags
PERIOD = []
try:
    program_tag = Tag.objects.get(name__iexact='Period')
    ACADEMIC_PROGRAMS = TaggedItem.objects.get_by_model(GenericChoice, program_tag).filter(active = True)
except:
    pass

PAY_GRADE = []
try:
    program_tag = Tag.objects.get(name__iexact='Pay Grade')
    ACADEMIC_PROGRAMS = TaggedItem.objects.get_by_model(GenericChoice, program_tag).filter(active = True)
except:
    pass

WORK_DAYS = []
try:
    program_tag = Tag.objects.get(name__iexact='Work Days')
    ACADEMIC_PROGRAMS = TaggedItem.objects.get_by_model(GenericChoice, program_tag).filter(active = True)
except:
    pass

class JobApplyForm(forms.ModelForm):
    job         = forms.ModelChoiceField(Post, required=False, widget=forms.HiddenInput())
    class Meta:
        model = JobApplyForm
        
class PostForm(forms.ModelForm):
    period              = models.ForeignKey(queryset=PERIOD, empty_label=None, widget=forms.RadioSelect()
    pay_grade           = models.ForeignKey(queryset=PAY_GRADE, empty_label=None, widget=forms.RadioSelect()
    work_days           = forms.ModelMultipleChoiceField(queryset=WORK_DAYS, widget=forms.CheckboxSelectMultiple())
    hiring_department   = models.ForeignKey(Department)
    publish             = forms.DateTimeField(help_text="A date for the post to go live on", widget=DateTimeWidget)
    expire_date         = forms.DateTimeField(help_text="A date for the post to expire on", widget=DateTimeWidget)
    
    class Meta:
        model = Post
        
    #Makes sure the user picks an expire date later than the post date
    def clean_date(self):
        postdate = self.cleaned_data['publish']
        expiredate = self.cleaned_data['expire_date']
        if postdate >= expiredate:
            raise forms.ValidationError("You must pick an expire date later than the post date!")
        return expiredate