from django import forms

from djforms.jobpost.models import *
from djforms.core.models import Department, GenericChoice, YEAR_CHOICES

from localflavor.us.forms import USPhoneNumberField

from tagging.models import Tag, TaggedItem

try:
    dept_tag = Tag.objects.get(name__iexact='Jobs')
    DEPARTMENTS = TaggedItem.objects.get_by_model(Department, dept_tag)
except:
    DEPARTMENTS = Department.objects.none()

try:
    period_tag = Tag.objects.get(name__iexact='Period')
    PERIOD = TaggedItem.objects.get_by_model(GenericChoice, period_tag).filter(active = True)
except:
    PERIOD = GenericChoice.objects.none()

try:
    pay_grade_tag = Tag.objects.get(name__iexact='Pay Grade')
    PAY_GRADE = TaggedItem.objects.get_by_model(GenericChoice, pay_grade_tag).filter(active = True)
except:
    PAY_GRADE = GenericChoice.objects.none()

try:
    work_day_tag = Tag.objects.get(name__iexact='Work Days')
    WORK_DAYS = TaggedItem.objects.get_by_model(GenericChoice, work_day_tag).filter(active = True)
except:
    WORK_DAYS = GenericChoice.objects.none()

try:
    type_of_job_tag = Tag.objects.get(name__iexact='Type of Job')
    TYPE_OF_JOB = TaggedItem.objects.get_by_model(GenericChoice, type_of_job_tag).filter(active = True)
except:
    TYPE_OF_JOB = GenericChoice.objects.none()

class JobApplyForms(forms.ModelForm):
    phone           = USPhoneNumberField(label="Phone", help_text="Format: XXX-XXX-XXXX")
    college_year    = forms.CharField(label="Year",widget=forms.Select(choices=YEAR_CHOICES))

    class Meta:
        model = JobApplyForm
        exclude = ('job',)

class PostFormWithHidden(forms.ModelForm):
    period              = forms.ModelChoiceField(queryset=PERIOD, empty_label=None, widget=forms.RadioSelect())
    pay_grade           = forms.ModelChoiceField(queryset=PAY_GRADE, empty_label=None, widget=forms.RadioSelect())
    work_days           = forms.ModelMultipleChoiceField(queryset=WORK_DAYS, widget=forms.CheckboxSelectMultiple())
    type_of_job         = forms.ModelChoiceField(queryset=TYPE_OF_JOB, empty_label=None, widget=forms.RadioSelect())
    hiring_department   = forms.ModelChoiceField(queryset=DEPARTMENTS)
    publish             = forms.DateTimeField(help_text="A date for the post to go live on")
    expire_date         = forms.DateTimeField(help_text="A date for the post to expire on")
    creator             = forms.ModelChoiceField(queryset=User.objects.all(), required=False, widget=forms.HiddenInput())
    active              = forms.BooleanField(help_text='Is active?', required=False, widget=forms.HiddenInput())

    class Meta:
        model = Post
        exclude = ('slug')

    #Makes sure the user picks an expire date later than the post date
    def clean_date(self):
        postdate = self.cleaned_data['publish']
        expiredate = self.cleaned_data['expire_date']
        if postdate >= expiredate:
            raise forms.ValidationError("You must pick an expire date later than the post date!")
        return expiredate

class PostFormWithoutHidden(forms.ModelForm):
    period              = forms.ModelChoiceField(queryset=PERIOD, empty_label=None, widget=forms.RadioSelect())
    pay_grade           = forms.ModelChoiceField(queryset=PAY_GRADE, empty_label=None, widget=forms.RadioSelect())
    work_days           = forms.ModelMultipleChoiceField(queryset=WORK_DAYS, widget=forms.CheckboxSelectMultiple())
    type_of_job         = forms.ModelChoiceField(queryset=TYPE_OF_JOB, empty_label=None, widget=forms.RadioSelect())
    hiring_department   = forms.ModelChoiceField(queryset=Department.objects.all())
    publish             = forms.DateTimeField(help_text="A date for the post to go live on")
    expire_date         = forms.DateTimeField(help_text="A date for the post to expire on")

    class Meta:
        model = Post
        exclude = ('creator',)

    #Makes sure the user picks an expire date later than the post date
    def clean_date(self):
        postdate = self.cleaned_data['publish']
        expiredate = self.cleaned_data['expire_date']
        if postdate >= expiredate:
            raise forms.ValidationError("You must pick an expire date later than the post date!")
        return expiredate

class PostFormMostHidden(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('num_positions', 'expire_date')
