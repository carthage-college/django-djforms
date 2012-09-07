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
    department      = forms.ModelChoiceField(queryset=DEPTS,required=False)

    class Meta:
        model = Presentation
        exclude = ('user','updated_by','date_created','date_updated','presenters','ranking','leader')


