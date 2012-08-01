from django import forms

from djforms.music.ensembles.choral.models import Candidate, TimeSlot

TIME_SLOTS = TimeSlot.objects.filter(active=True)

class CandidateForm(forms.ModelForm):

    time_slot = forms.ModelChoiceField(queryset=TIME_SLOTS)

    class Meta:
        model = Candidate
        exclude = ('user','created_on','updated_on',)

