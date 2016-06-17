from django import forms
from django.forms import ModelForm

from djforms.communications.metamorphosis.models import Questionnaire


class ParentQuestionnaireForm(forms.ModelForm):
    your_name = forms.CharField(
        label = "Your name",
        max_length=128,
        required = True
    )
    email = forms.EmailField(
        label = "Your email address",
        max_length=128
    )
    how_changed = forms.CharField(
        label = """
            How has your student changed since his or her freshman year?
        """,
        widget = forms.Textarea
    )
    comments = forms.CharField(
        label = "Additional comments?",
        widget = forms.Textarea
    )

    class Meta:
        model = Questionnaire
        exclude = ('photos','status')

class StudentQuestionnaireForm(forms.ModelForm):
    student_name = forms.CharField(
        label = "Your name",
        max_length=128,
        required = True
    )
    email = forms.EmailField(
        label = "Your email address",
        max_length=128
    )
    how_changed = forms.CharField(
        label = """
            How have you changed since freshman year?
        """,
        widget = forms.Textarea
    )
    comments = forms.CharField(
        label = "Additional comments?",
        widget = forms.Textarea
    )

    class Meta:
        model = Questionnaire
        exclude = ('your_name','photos','status')
        fields = ('student_name','email','hometown','how_changed','comments')
