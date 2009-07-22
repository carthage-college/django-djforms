from django import forms
from djforms.eduform.models import EduProfile
from djforms.eduform.models import GenericChoice
from tagging.models import Tag, TaggedItem

PROGRAMS_OF_INTEREST = []
try:
    program_tag = Tag.objects.get(name='Programs Of Interest')
    programs = TaggedItem.objects.get_by_model(GenericChoice, program_tag)
    for p in programs.filter(active = True):
        PROGRAMS_OF_INTEREST.append((p.id,p.value))
except:
    pass

class EduProfileForm(forms.ModelForm):
    programs_of_interest = forms.MultipleChoiceField(choices=PROGRAMS_OF_INTEREST, widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = EduProfile

    def clean_programs_of_interest(self):
        if len(self.cleaned_data['programs_of_interest']) < 1:
            raise forms.ValidationError('Select at least one Program of Interest.')
        return self.cleaned_data['programs_of_interest']