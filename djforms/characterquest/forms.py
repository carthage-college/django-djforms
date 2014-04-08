from django import forms
from django.forms import ModelForm
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.contrib.localflavor.us.forms import USZipCodeField
from djforms.characterquest.models import ApplicationProfile
from djforms.core.models import UserProfile, BINARY_CHOICES
from djforms.core.models import GENDER_CHOICES, STATE_CHOICES, YEAR_CHOICES

class ApplicationProfileForm(forms.ModelForm):
    address = forms.CharField(label="Permanent Address")
    city    = forms.CharField()
    state   = forms.CharField(
        widget=forms.Select(choices=STATE_CHOICES), required=True
    )
    zip = USZipCodeField()
    phone = USPhoneNumberField(label="Cell Phone")
    gender = forms.CharField(
        widget=forms.RadioSelect(choices=GENDER_CHOICES)
    )
    dob = forms.DateField(label="Birthday")
    campus_address = forms.CharField()
    campus_box = forms.CharField(max_length="4")
    college_id = forms.CharField(label="Carthage ID", max_length="7")
    college_year = forms.CharField(
        label="Year",widget=forms.Select(choices=YEAR_CHOICES)
    )

    class Meta:
        model = UserProfile
        exclude = ('permission','latitude','longitude','location','user',
                   'creation_at','updated_at','country')
        fields = ['address','city','state','zip','phone','gender','dob',
                  'campus_address', 'campus_box','college_id','college_year']

class ApplicationForm(forms.ModelForm):

    class Meta:
        model = ApplicationProfile
        exclude = ('profile',)
        fields = [
            'organizations','skills_experience','why_orientation_leader',
            'describe_experience','references'
        ]
