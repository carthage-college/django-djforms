# -*- coding: utf-8 -*-

import datetime

from captcha.fields import CaptchaField
from django import forms
from djforms.alumni.classnotes.models import Contact
from djtools.fields import REQ_CSS
from djtools.fields import YEARS1
from djtools.fields import YEARS4

CLASSYEARS  = list(YEARS4)
SPOUSEYEARS = list(YEARS1)

CLASSYEARS.insert(0, ('', 'Your class'))
CLASSYEARS.insert(1, ('1847', 'Friend of Carthage'))
SPOUSEYEARS.insert(0, ('', "Spouse's class"))
REQ=REQ_CSS
CATEGORIES = (
    ('', '-------------'),
    ('Birth/Adoption Announcement', 'Birth/Adoption Announcement'),
    ('Career Update', 'Career Update'),
    ('Death Announcement', 'Death Announcement'),
    ('Marriage Announcement', 'Marriage Announcement'),
    ('Personal Achievement', 'Personal Achievement'),
    ('Other News', 'Other News'),
)


class ContactForm(forms.ModelForm):
    classyear = forms.CharField(
        label="Class", max_length=4,
        widget=forms.Select(choices=CLASSYEARS),
    )
    spouseyear = forms.CharField(
        label="Spouse's class", max_length=4,
        widget=forms.Select(choices=SPOUSEYEARS),
        required=False,
    )
    email = forms.EmailField(
        label="Email",
        required=False,
    )
    classnote = forms.CharField(
        widget=forms.Textarea,
        label="Your message to the Carthage community",
        required=True,
    )
    category = forms.CharField(
        label="Category",
        widget=forms.Select(choices=CATEGORIES, attrs=REQ),
        required=True,
    )
    captcha = CaptchaField()

    class Meta:
        model = Contact
        exclude = (
            'alumnistatus',
            'pubstatus',
            'pubstatusdate',
            'carthaginianstatus',
            'pubtext',
            'alumnicomments',
        )
        fields = (
            'salutation',
            'first_name',
            'second_name',
            'last_name',
            'suffix',
            'previous_name',
            'email',
            'classyear',
            'spousename',
            'spousepreviousname',
            'spouseyear',
            'hometown',
            'classnote',
            'category',
            'picture',
            'caption',
        )
