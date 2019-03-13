from django import forms
from django.forms import ModelForm

from djforms.alumni.memory.models import Questionnaire

from djtools.fields import YEARS1
from djtools.fields.localflavor import USPhoneNumberField

from localflavor.us.forms import USZipCodeField

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
            'greek_siblings','special','relive','message',
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

class PiTheta50thReunion(QuestionnaireForm):

    greek_parent = forms.CharField(
        label="Who is your Pi Theta mom?",
        required = True
    )
    greek_siblings = forms.CharField(
        label = "Who is your Pi Theta daughter(s)?",
        widget = forms.Textarea,
        required = True
    )
    special = forms.CharField(
        label = "What was your favorite Pi Theta tradition?",
        widget = forms.Textarea,
        required = True
    )
    relive = forms.CharField(
        label = """
            If you had the chance to relive a single
            Pi Theta moment, which one would you choose?
        """,
        widget = forms.Textarea,
        required = True
    )

class KappaChiOmega50thReunion(QuestionnaireForm):

    greek_parent = forms.CharField(
        label="Who is your Kappa Chi Omega mom?",
        required = True
    )
    greek_siblings = forms.CharField(
        label = "Who is your Kappa Chi Omega daughter(s)?",
        widget = forms.Textarea,
        required = True
    )
    special = forms.CharField(
        label = "What was your favorite Kappa Chi Omega tradition?",
        widget = forms.Textarea,
        required = True
    )
    relive = forms.CharField(
        label = """
            If you had the chance to relive a single
            Kappa Chi Omega moment, which one would you choose?
        """,
        widget = forms.Textarea,
        required = True
    )
