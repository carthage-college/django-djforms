# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from djforms.prehealth.committee_letter.models import Applicant
from djforms.prehealth.committee_letter.models import Recommendation
from djforms.prehealth.committee_letter.forms import PROGRAM_CHOICES


class RecommendationInline(admin.TabularInline):
    """Custom admin class for recommendation letters."""

    model = Recommendation
    fields = ('name', 'email')


class ApplicantAdminForm(forms.ModelForm):
    """Custom admin form for applicant data model."""

    class Meta:
        """Sub-class for defining settings about the parent class."""

        model = Applicant
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """Override the init method to provide program choices."""
        super(ApplicantAdminForm, self).__init__(*args, **kwargs)
        self.fields['programs_apply'].queryset = PROGRAM_CHOICES


class ApplicantAdmin(admin.ModelAdmin):
    """Admin class for the applicants data model."""

    model = Applicant
    form = ApplicantAdminForm
    filter_horizontal = ('programs_apply',)
    list_display  = (
        'last_name',
        'first_name',
        'created_on',
        'email',
        'city',
        'state',
        'phone',
        'cv_link',
        'personal_statements_link',
        'transcripts_link',
        'waiver_link',
    )
    date_hierarchy = 'created_on'
    ordering = (
        'created_on',
        'created_by__last_name',
        'created_by__email',
        'programs_apply',
        'first_generation',
    )
    list_filter = ('programs_apply', 'first_generation')
    search_fields = (
        'created_by__last_name',
        'created_by__email',
        'created_by__username',
    )
    raw_id_fields = ('created_by', 'updated_by')
    list_per_page = 500
    inlines = [RecommendationInline]

    def cv_link(self, instance):
        """Display method for the CV file."""
        code = None
        if instance.cv:
            code = mark_safe('<a href="{0}" target="_blank">CV</a>'.format(
                instance.cv.url,
            ))
        return code
    cv_link.allow_tags = True
    cv_link.short_description = "CV"

    def personal_statements_link(self, instance):
        """Display method to provide a link to the personal statement."""
        code = None
        if instance.personal_statements:
            code =  mark_safe('<a href="{0}" target="_blank">Statements</a>'.format(
                instance.personal_statements.url,
            ))
        return code
    personal_statements_link.allow_tags = True
    personal_statements_link.short_description = "Personal Statements"

    def transcripts_link(self, instance):
        """Display method to provide a link to the transcript."""
        code = None
        if instance.transcripts:
            code =  mark_safe('<a href="{0}" target="_blank">Transcripts</a>'.format(
                instance.transcripts.url,
            ))
        return code
    transcripts_link.allow_tags = True
    transcripts_link.short_description = "Transcripts"

    def waiver_link(self, instance):
        """Display method to provide a link to the waiver."""
        code = None
        if instance.waiver:
            code =  mark_safe('<a href="{0}" target="_blank">Waiver</a>'.format(
                instance.waiver.url,
            ))
        return code
    waiver_link.allow_tags = True
    waiver_link.short_description = "Waiver"

    def save_model(self, request, obj, form, change):
        """Override save method to provide the user who updated the object."""
        if change:
            obj.updated_by = request.user
        obj.save()

admin.site.register(Applicant, ApplicantAdmin)
