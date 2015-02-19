from django import forms
from django.forms import ModelForm

from djforms.alumni.memory.models import Questionnaire
from djtools.fields import YEARS1

from localflavor.us.forms import USPhoneNumberField, USZipCodeField
from captcha.fields import CaptchaField

CLASSYEARS  = list(YEARS1)
CLASSYEARS.insert(0,("","--select--"))


class QuestionnaireForm(forms.ModelForm):
    second_name = forms.CharField(
        label = "Maiden name",
        required = False
    )
    phone = USPhoneNumberField()
    postal_code = USZipCodeField(label="Zip code")
    class_year = forms.CharField(
        label="Your class year",
        widget=forms.Select(choices=CLASSYEARS),
    )
    email = forms.EmailField()
    greek_parent = forms.CharField(
        required = True
    )
    greek_siblings = forms.CharField(
        required = True
    )
    captcha = CaptchaField(
        label = """
            Input the text you see in the image on the left
        """,
        required = True
    )

    class Meta:
        model = Questionnaire
        exclude = (
            'photos','promotion','professor','professor_why',
            'why_carthage'
        )
        fields = (
            'first_name','second_name','last_name','class_year',
            'address1','address2','city','state','postal_code','phone','email',
            'occupation1','occupation2','greek_parent',
            'greek_siblings','special','relive','message','captcha'
        )


class KappaPhiEta50thReunion(QuestionnaireForm):

    greek_parent = forms.CharField(
        label="Who is your Kappa Phi Eta mom?",
        required = True
    )
    greek_siblings = forms.CharField(
        label = "Who is your Kappa Phi Eta daughter(s)?",
        widget = forms.Textarea,
        required = True
    )
    special = forms.CharField(
        label = "What was your favorite Kappa Phi Eta tradition?",
        widget = forms.Textarea,
        required = True
    )
    relive = forms.CharField(
        label = """
            If you had the chance to relive a single
            Kappa Phi Eta moment, which one would you choose?
        """,
        widget = forms.Textarea,
        required = True
    )

