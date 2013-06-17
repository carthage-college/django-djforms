from django import forms

STATUS = (
    ("Freshman","Freshman"),
    ("Transfer","Transfer"),
)

GPA_SCALE = (
    ("4.0","4.0"),
    ("5.0","5.0"),
    ("6.0","6.0"),
    ("7.0","7.0"),
    ("8.0","8.0"),
    ("9.0","9.0"),
    ("10.0","10.0"),
    ("11.0","11.0"),
    ("12.0","12.0"),
    ("100","100"),
)

class ChanceOfForm(forms.Form):
    first_name      = forms.CharField()
    email           = forms.EmailField()
    confirm_email   = forms.EmailField()
    status          = forms.TypedChoiceField(choices=STATUS, widget=forms.RadioSelect())
    act_sat         = forms.CharField(label="ACT or SAT", help_text="(SAT=Critical Reading + Math)")
    gpa             = forms.CharField(label="GPA", max_length=4)
    gpa_scale       = forms.TypedChoiceField(label="GPA Scale", choices=GPA_SCALE, widget=forms.Select())
    information     = forms.CharField(label="Aditional Information", help_text="i.e. extracurriculars, AP, etc.", widget=forms.Textarea, required=False)
    prospect_status = forms.CharField(widget=forms.HiddenInput(), required=False)

    def clean_confirm_email(self):
        cleaned_data = self.cleaned_data
        email1 = cleaned_data.get("email")
        email2 = cleaned_data.get("confirm_email")
        if email1 != email2:
            raise forms.ValidationError("Emails do not match")

        return cleaned_data["confirm_email"]

    def __init__(self, *args, **kwargs):
        super(ChanceOfForm, self).__init__(*args, **kwargs)
