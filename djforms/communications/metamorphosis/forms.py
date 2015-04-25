from django import forms
from django.forms import ModelForm

from djforms.communications.metamorphosis.models import Questionnaire

from captcha.fields import CaptchaField


class QuestionnaireForm(forms.ModelForm):
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
    captcha = CaptchaField(
        label = """
            Input the text you see in the image on the left
        """
    )

    class Meta:
        model = Questionnaire
        exclude = ('photos','status')
