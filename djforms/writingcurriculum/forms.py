from django import forms
from django.forms import ModelForm
from djforms.core.models import BINARY_CHOICES, GenericChoice
from djforms.writingcurriculum.models import CourseProposal, DAY_SPS_CHOICES

from tagging.models import Tag, TaggedItem

try:
    period_tag = Tag.objects.get(name__iexact='Period')
    PERIOD = TaggedItem.objects.get_by_model(
        GenericChoice, period_tag
    ).filter(active = True)
except:
    PERIOD = GenericChoice.objects.none()

class ProposalForm(forms.ModelForm):
    academic_term = forms.ModelChoiceField(
        empty_label = None,
        queryset = PERIOD, widget=forms.RadioSelect()
    )
    day_sps = forms.ChoiceField(
        label = "Day or SPS",
        choices = DAY_SPS_CHOICES, widget=forms.RadioSelect()
    )
    approved_wi = forms.ChoiceField(
        label = "Approved Writing Intensive Course?",
        choices = BINARY_CHOICES, widget=forms.RadioSelect(),
        help_text = """
            This course has been approved by the appropriate
            department as a Writing Intensive Course.
        """
    )
    workshop = forms.ChoiceField(
        label = "Writing Intensive Workshop",
        choices = BINARY_CHOICES, widget=forms.RadioSelect(),
        help_text = """
            Before an instructor teaches a Writing Intensive course,
            she must have completed a Writing Intensive workshop. Have you?
        """
    )
    permission = forms.ChoiceField(
        label = "Permission to Include Syllabus in WAC Archive",
        choices = BINARY_CHOICES, widget=forms.RadioSelect(),
        help_text = """
            Do you grant the WAC Committee permission to add your syllabus
            to our public archive of syllabi for Writing Intensive courses?
        """
    )

    class Meta:
        model = CourseProposal
        exclude = (
            'user','updated_by','date_created','date_updated','criteria'
        )

    def clean_when_approved_wi(self):
        if self.cleaned_data.get('approved_wi') == "No" \
          and not self.cleaned_data.get('when_approved_wi'):
            raise forms.ValidationError("""
                You must provide a date when the course will be approved
                by the department.
            """)
        return self.cleaned_data['when_approved_wi']

    def clean_when_workshop(self):
        if self.cleaned_data.get('workshop') == "No" \
          and not self.cleaned_data.get('when_workshop'):
            raise forms.ValidationError("""
                You must provide a date by which time you will have completed
                a Writing Intensive workshop.
            """)
        return self.cleaned_data['when_workshop']
