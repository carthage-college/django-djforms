from django import forms
from djforms.admissions.visitdays.models import VisitDayBaseProfile

class VisitDayBaseForm(forms.ModelForm):
    class Meta:
        model = VisitDayBaseProfile

