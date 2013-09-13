# -*- coding: utf-8 -*-
from django import forms
from django.contrib.localflavor.us.forms import USPhoneNumberField, USZipCodeField

from djforms.admissions.admitted.models import *

GENDER_CHOICES = (
    ('Female (女)','Female (女)'),
    ('Male (男)','Male (男)'),
)
LEVEL_CHOICES = (
    ('Undergraduate Freshman','Undergraduate Freshman'),
    ('Undergraduate Transfer','Undergraduate Transfer'),
    ('Graduate Student','Graduate Student'),
)
HELP_CHOICES = (
    ('I am interested in scheduling an admission and scholarship interview in China',
     'I am interested in scheduling an admission and scholarship interview in China',),
    ('I am interested in scheduling a musical theatre audition in China',
     'I am interested in scheduling a musical theatre audition in China'),
    ('I would like to receive more information about your programs',
     'I would like to receive more information about your programs',)
)
UNDERGRADUATE_DEGREES = (
    ('Accounting','Accounting'),
    ('Art - Art History','Art - Art History'),
    ('Art - Studio Art','Art - Studio Art'),
    ('Asian Studies','Athletic Training'),
    ('Biology','Biology'),
    ('Business','Business'),
    ('Chemistry','Chemistry'),
    ('Chinese','Chinese'),
    ('Classical Archaeology','Classical Archaeology'),
    ('Classical Foundations','Classical Foundations'),
    ('Classical Studies','Classical Studies'),
    ('Communication','Communication'),
    ('Computer Science','Computer Science'),
    ('Criminal Justice','Criminal Justice'),
    ('Economics','Economics'),
    ('Education - Special Education (Grades K-12)','Education - Special Education (Grades K-12)'),
    ('Education - Elementary/Middle Education (Grades 1-8)','Education - Elementary/Middle Education (Grades 1-8)'),
    ('Education - Middle/Secondary Education (Grades 6-12)','Education - Middle/Secondary Education (Grades 6-12)'),
    ('English','English'),
    ('English with emphasis in Creative Writing','English with emphasis in Creative Writing'),
    ('Environmental Science','Environmental Science'),
    ('Finance','Finance'),
    ('French','French'),
    ('Geography & Earth Science','Geography & Earth Science'),
    ('German','German'),
    ('Graphic Design','Graphic Design'),
    ('Great Ideas','Great Ideas'),
    ('History','History'),
    ('International Political Economy','International Political Economy'),
    ('Japanese','Japanese'),
    ('Management','Management'),
    ('Marketing','Marketing'),
    ('Mathematics','Mathematics'),
    ('Music','Music'),
    ('Music - Church Music','Music - Church Music'),
    ('Music - Instrumental Music Education','Music - Instrumental Music Education'),
    ('Music - Jazz Studies','Music - Jazz Studies'),
    ('Music - Performance','Music - Performance'),
    ('Music - Piano Pedagogy','Music - Piano Pedagogy'),
    ('Music - Vocal Music Education','Music - Vocal Music Education'),
    ('Music Theatre','Music Theatre'),
    ('Neuroscience','Neuroscience'),
    ('Philosophy','Philosophy'),
    ('Physical Education','Physical Education'),
    ('Physical Education, Sport and Fitness Instruction','Physical Education, Sport and Fitness Instruction'),
    ('Physics','Physics'),
    ('Political Science','Political Science'),
    ('Psychology','Psychology'),
    ('Public Relations','Public Relations'),
    ('Religion','Religion'),
    ('Social Science','Social Science'),
    ('Social Work','Social Work'),
    ('Sociology','Sociology'),
    ('Spanish','Spanish'),
    ('Theatre','Theatre'),
    ('Theatre - Performance','Theatre - Performance'),
    ('Theatre - Technical Production and Design','Theatre - Technical Production and Design'),
    ('Self-Designed Major','Self-Designed Major'),
)
GRADUATE_DEGREES = (
    ('Business (MBA)','Business (MBA)'),
    ('Education','Education'),
)

class InterestForm(forms.Form):
    last_name       = forms.CharField(label="Last name (姓)")
    first_name      = forms.CharField(label="First name (名)")
    dob             = forms.DateField(label="Birthday (出生日)",help_text="(MM/DD/YYYY) (月月／日日／年年年年)")
    gender          = forms.TypedChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect())
    address         = forms.CharField(label='Home address (家庭地址)',max_length=255,widget=forms.TextInput())
    city            = forms.CharField(label='City (城市)',max_length=128,widget=forms.TextInput())
    postal_code     = forms.CharField(label='Postal code (邮政编码)', max_length='6')
    country         = forms.CharField(label='Country (国家)',max_length=128)
    email           = forms.EmailField(label='Email address (电子邮件信箱)')
    phone           = forms.CharField(label='Telephone number (电话)',max_length=18)
    mobile          = forms.CharField(label='Cell phone number (手机号码)',max_length=18,required=False)
    level           = forms.TypedChoiceField(label="Entering level",choices=LEVEL_CHOICES,widget=forms.RadioSelect())
    how_help        = forms.MultipleChoiceField(label="How may we help you? Check all that apply.",choices=HELP_CHOICES,widget=forms.CheckboxSelectMultiple())
    undergrad       = forms.MultipleChoiceField(label="Undergraduate degree interest. Check all that apply.",choices=UNDERGRADUATE_DEGREES,widget=forms.CheckboxSelectMultiple())
    graduate        = forms.MultipleChoiceField(label="Graduate degrees. Check all that apply.",choices=GRADUATE_DEGREES,widget=forms.CheckboxSelectMultiple())

