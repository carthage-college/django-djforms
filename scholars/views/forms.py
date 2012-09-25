from django import forms
from django.forms import ModelForm
from djforms.core.models import GenericChoice
from djforms.scholars.models import Presentation
from djforms.core.models import Department

from tagging.models import Tag, TaggedItem

try:
    dept_tag = Tag.objects.get(name__iexact='WAC')
    DEPTS = TaggedItem.objects.get_by_model(Department, dept_tag)
except:
    DEPTS = Department.objects.none()


class PresentationForm(forms.ModelForm):

    class Meta:
        model = Presentation
        exclude = ('user','updated_by','date_created','date_updated','presenters','ranking','leader','status')

    def __init__(self,*args,**kwargs):
        super(PresentationForm,self).__init__(*args,**kwargs)
        self.fields.keyOrder = ['title','funding','requirements','work_type','permission','shared',
        'abstract_text','abstract_file','poster_file','tags']
