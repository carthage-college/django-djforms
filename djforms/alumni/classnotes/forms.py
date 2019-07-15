from django import forms

from djtools.fields import YEARS1, YEARS4, REQ_CSS
from djforms.alumni.classnotes.models import Contact

from captcha.fields import CaptchaField
#from captcha.fields import ReCaptchaField

import datetime

CLASSYEARS  = list(YEARS4)
SPOUSEYEARS = list(YEARS1)

CLASSYEARS.insert(0,("","Your class"))
CLASSYEARS.insert(1,("1847","Friend of Carthage"))
SPOUSEYEARS.insert(0,("","Spouse's class"))
REQ=REQ_CSS
CATEGORIES = (
    ('','-------------'),
    ('Marriage Announcement','Marriage Announcement'),
    ('Birth/Adoption Announcement','Birth/Adoption Announcement'),
    ('Death Announcement','Death Announcement'),
    ('Other News','Other News'),
)


class ContactForm(forms.ModelForm):
    classyear = forms.CharField(
        label="Class", max_length=4,
        widget=forms.Select(choices=CLASSYEARS)
    )
    spouseyear = forms.CharField(
        label="Spouse's class", max_length=4,
        widget=forms.Select(choices=SPOUSEYEARS),
        required=False
    )
    email = forms.EmailField(
        label="Email",
        required=False
    )
    classnote = forms.CharField(
        widget=forms.Textarea,
        label="Your message to the Carthage community",
        required=True
    )
    category = forms.CharField(
        label="Category",
        widget=forms.Select(choices=CATEGORIES, attrs=REQ),
        required=True
    )
    captcha = CaptchaField()

    class Meta:
        model = Contact
        exclude = (
            'alumnistatus','pubstatus','pubstatusdate','carthaginianstatus',
            'pubtext','alumnicomments'
        )

    def __init__(self,*args,**kwargs):
        super(ContactForm,self).__init__(*args,**kwargs)
        self.fields.keyOrder = [
            'salutation','first_name','second_name','last_name','suffix',
            'previous_name','email','classyear','spousename',
            'spousepreviousname','spouseyear','hometown','classnote',
            'category','picture','caption'
        ]

