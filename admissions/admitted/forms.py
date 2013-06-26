from django import forms
from djforms.admissions.admitted.models import *

class ChanceOfForm(forms.ModelForm):
    first_name      = forms.CharField()
    email           = forms.EmailField()
    confirm_email   = forms.EmailField()
    status          = forms.TypedChoiceField(choices=STATUS, widget=forms.RadioSelect(), initial="Freshman")
    act_sat         = forms.CharField(label="ACT or SAT", help_text="(SAT=Critical Reading + Math)")
    gpa             = forms.CharField(label="GPA", max_length=4)
    gpa_scale       = forms.TypedChoiceField(label="GPA Scale", choices=GPA_SCALE, widget=forms.Select())
    information     = forms.CharField(label="Aditional Information", help_text="i.e. extracurriculars, AP, etc.", widget=forms.Textarea, required=False)
    prospect_status = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model       = Candidate
        fields      = ('first_name','email','confirm_email','status','act_sat','gpa','gpa_scale','information','prospect_status')

    def clean_confirm_email(self):
        cleaned_data = self.cleaned_data
        email1 = cleaned_data.get("email")
        email2 = cleaned_data.get("confirm_email")
        if email1 != email2:
            raise forms.ValidationError("Emails do not match")

        return cleaned_data["confirm_email"]

