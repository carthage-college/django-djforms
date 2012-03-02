from django import forms

class NightReportForm(forms.Form):
    """
    A form to collect participant info and conditions at the Griffin Observatory
    """
    date                = forms.DateField(label = "Date (start of night)")
    name                = forms.CharField(label = "Observer name(s)", max_length=255)
    email               = forms.EmailField()
    organization        = forms.CharField(label = "Oranization(s)", max_length=255)
    guests              = forms.CharField(max_length=3, label="Number of Guests")
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

