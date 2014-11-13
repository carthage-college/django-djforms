from django import forms

from djtools.fields import STATE_CHOICES, YEARS1, REQ_CSS
from djforms.alumni.classnotes.models import Contact

from localflavor.us.forms import USPhoneNumberField, USZipCodeField

from captcha.fields import CaptchaField

import datetime

CLASSYEARS  = list(YEARS1)
SPOUSEYEARS = list(YEARS1)

CLASSYEARS.insert(0,("","Your class"))
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
        widget=forms.Select(choices=CLASSYEARS, attrs=REQ),
        required=True
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
    captcha = CaptchaField(required=True)

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
            'category','picture','caption','captcha'
        ]

