from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField
from djforms.characterquest.models import EnrollmentProfile, SHIRT_SIZE_CHOICES,BINARY_CHOICES
from djforms.core.models import UserProfile, SEX_CHOICES, STATE_CHOICES, YEAR_CHOICES

class EnrollmentProfileForm(forms.ModelForm):
    address = forms.CharField(label="Permanent Address")
    city    = forms.CharField()
    state   = forms.CharField(widget=forms.Select(choices=STATE_CHOICES), required=True)
    zip     = USZipCodeField()
    phone   = USPhoneNumberField(label="Cell Phone")
    sex     = forms.CharField(widget=forms.RadioSelect(choices=SEX_CHOICES))
    dob     = forms.DateField(label="Birthday")
    campus_address = forms.CharField()
    campus_box = forms.CharField(max_length="4")
    college_access_code = forms.CharField(label="Carthage Access Code",max_length="7")
    college_id = forms.CharField(label="Carthage ID", max_length="7")
    college_year = forms.CharField(label="Year",widget=forms.Select(choices=YEAR_CHOICES))

    class Meta:
        model = UserProfile
        exclude = ('permission','latitude','longitude','location','user',
                   'creation_date','country')
        fields = ['address','city','state','zip','phone','sex','dob',
                  'campus_address', 'campus_box','college_access_code',
                  'college_id','college_year']

class EnrollmentForm(forms.ModelForm):

    class Meta:
        model = EnrollmentProfile
        exclude = ('profile',)
        fields = ['organizations','skills_experience','why_orientation_leader','describe_experience']
