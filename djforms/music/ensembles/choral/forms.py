from django import forms

from djforms.music.ensembles.choral.models import Candidate, TimeSlot

TIME_SLOTS = TimeSlot.objects.filter(active=True).order_by('id')

class CandidateForm(forms.ModelForm):

    time_slot = forms.ModelChoiceField(queryset=TIME_SLOTS)

    class Meta:
        model   = Candidate
        exclude = ('user','created_on','updated_on',)

class ManagerForm(CandidateForm):

    first_name          = forms.CharField(max_length=128)
    last_name           = forms.CharField(max_length=128)
    email               = forms.EmailField()

    class Meta:
        model   = Candidate
        exclude = ('user','created_on','updated_on',)
        fields  = (
            'first_name','last_name','email','time_slot','majors',
            'grad_year','experience'
        )

