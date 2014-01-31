from django import forms
from django.forms import ModelForm
from djforms.core.models import GenericChoice
from djforms.scholars.models import Presentation
from djforms.core.models import Department, BINARY_CHOICES

from tagging.models import Tag, TaggedItem

try:
    dept_tag = Tag.objects.get(name__iexact='WAC')
    DEPTS = TaggedItem.objects.get_by_model(Department, dept_tag)
except:
    DEPTS = Department.objects.none()


class PresentationForm(forms.ModelForm):

    permission          = forms.ChoiceField(label="Permission to reproduce", choices=BINARY_CHOICES, widget=forms.RadioSelect(), help_text="Do you grant Carthage permission to reproduce your presentation?")
    shared              = forms.ChoiceField(label="Faculty sponsor approval", choices=BINARY_CHOICES, widget=forms.RadioSelect(), help_text='Has your faculty sponsor approved your proposal? Note: Faculty and staff presenters should choose "yes".')
    need_table          = forms.ChoiceField(label="Do you need a table for display purposes?", choices=BINARY_CHOICES, widget=forms.RadioSelect())
    need_electricity    = forms.ChoiceField(label="Do you need electricity for computer or other device?", choices=BINARY_CHOICES, widget=forms.RadioSelect())

    class Meta:
        model = Presentation
        exclude = ('user','updated_by','date_created','date_updated',
        'presenters','ranking','leader','status','work_type_other','tags')

    def __init__(self,*args,**kwargs):
        super(PresentationForm,self).__init__(*args,**kwargs)
        self.fields.keyOrder = ['title','funding','work_type','permission','shared',
        'abstract_text','need_table', 'need_electricity','poster_file']

class EmailPresentersForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, label="Email content")

