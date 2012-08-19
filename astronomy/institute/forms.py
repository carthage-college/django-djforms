from django import forms
from django.contrib.localflavor.us.forms import USZipCodeField
from djforms.core.models import STATE_CHOICES, BINARY_CHOICES

EDUCATION = (
    ("","---select---"),
    ("High school","High school"),
    ("Some college or technical education","Some college or technical education"),
    ("Associate's or technical degree","Associate's or technical degree"),
    ("BA/BS degree","BA/BS degree"),
    ("MA/MS or other post-college degree","MA/MS or other post-college degree"),
)

PROGRAM_CHOICES = (
    ("","---select---"),
    ("No","No"),
    ("High school coursework","High school coursework"),
    ("College coursework","College coursework"),
    ("Both high school and college","Both high school and college"),
    ("Other programs or activities","Other programs or activities"),
)

INTEREST_CHOICES = (
    ("A great deal","A great deal"),
    ("Some","Some"),
    ("Not much","Not much"),
    ("None","None"),
)

LEARNING_EXPERIENCE = (
    ("Excellent","Excellent"),
    ("Very good","Very good"),
    ("Good","Good"),
    ("Fair","Fair"),
    ("Poor","Poor"),
)

MOTIVATION = (
    ("A great deal", "A great deal"),
    ("Somewhat", "Somewhat"),
    ("Very little", "Very little"),
)

ONETOTEN = [(x, x) for x in xrange(1, 10)]

class NightReportForm(forms.Form):
    """
    A form to collect participant info and conditions at the Griffin Observatory
    """
    date                = forms.DateField(label = "Date (start of night)")
    name                = forms.CharField(label = "Observer name(s)", max_length=255)
    email               = forms.EmailField()
    organization        = forms.CharField(label = "Oranization(s)", max_length=255)
    guests              = forms.CharField(label = "Number of Guests (including yourself)", widget=forms.Select(choices=ONETOTEN))
    hours_available     = forms.CharField(max_length=2)
    hours_used          = forms.CharField(max_length=2)
    hours_lost1         = forms.CharField(label = "Hours lost (weather)", max_length=2)
    hours_lost2         = forms.CharField(label = "Hours lost (maintenance)", max_length=2)
    temp_open           = forms.CharField(label = "Temperature at open", help_text = "(fahrenheit)", max_length=2)
    humid_open          = forms.CharField(label = "Humidity at open", help_text = "(% percent)", max_length=2)
    temp_close          = forms.CharField(label = "Temperature at close ", help_text = "(fahrenheit)", max_length=2)
    humid_close         = forms.CharField(label = "Humidity at close", help_text = "(% percent)", max_length=2)
    problems            = forms.CharField(label = "Report Any Problems Encountered", widget=forms.Textarea, required=False)
    comments            = forms.CharField(help_text = "Summarize the Observing Session&mdash;How successful was it?", widget=forms.Textarea)


class EvaluationForm(forms.Form):
    """
    A form to collect evaluations at the Griffin Observatory
    """
    name                = forms.CharField(label = "Name", max_length=255)
    address             = forms.CharField(label = "Street Address")
    city                = forms.CharField(label = "City")
    state               = forms.CharField(label = "State", widget=forms.Select(choices=STATE_CHOICES))
    postal_code         = USZipCodeField (label = "Zip Code")
    email               = forms.EmailField()
    organization        = forms.CharField(label = "Oranization(s)", max_length=255, required=False)
    attending           = forms.CharField(label = "Number attending (including yourself)", widget=forms.Select(choices=ONETOTEN))
    education           = forms.CharField(label = "Education level", widget=forms.Select(choices=EDUCATION))
    past_programs       = forms.ChoiceField(label = "Have you participated in other programs in the past?", choices=BINARY_CHOICES, widget=forms.RadioSelect())
    programs_activity   = forms.CharField(label = "If yes, please list the programs and/or activities.", max_length=255, required=False)
    prior_experience    = forms.CharField(label = "Astronomy/Physics experience", help_text = "Have you participated in programs or activities related to astronomy or physics besides this program?", widget=forms.Select(choices=PROGRAM_CHOICES))
    other_experience    = forms.CharField(label = "If other, please list them.", max_length=255)
    interest            = forms.ChoiceField(label = "Interest in astronomy and physics", help_text = "Overall, how much interest would you say you had prior to this program in topics related to astronomy and physics?", choices=INTEREST_CHOICES, widget=forms.RadioSelect())
    rate_learning       = forms.ChoiceField(label = "Rate your learning experience", help_text = "All in all, how would you rate your learning experience in this program?", choices=LEARNING_EXPERIENCE, widget=forms.RadioSelect())
    reinforced          = forms.ChoiceField(label = "Knowledge of astronomy", help_text = "Did this program strengthen your knowledge of astronomy?", choices=MOTIVATION, widget=forms.RadioSelect())
    motivation          = forms.ChoiceField(label = "Further study", help_text = "Did this program motivate you to learn more about astronomy?", choices=MOTIVATION, widget=forms.RadioSelect())
    study_comments      = forms.CharField (label  = "Please elaborate", widget=forms.Textarea, required=False)
    dependence          = forms.ChoiceField(label = "Dependence on astronomy", help_text = "Do you agree that this program helped you understand how life and other features of our planet depend upon astronomical processes?", choices=ONETOTEN, widget=forms.RadioSelect())

