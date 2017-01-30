# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from djtools.fields import BINARY_CHOICES
from djtools.fields.helpers import upload_to_path
from djtools.fields.validators import MimetypeValidator
from djtools.fields.validators import credit_gpa_validator

PROGRAMS_CHOICES = (
    ("DO","D.O."),
    ("DDS","D.D.S."),
    ("MD","M.D"),
    ("MDPhD","M.D./Ph.D")
)


class Applicant(models.Model):
    '''
    Data model for Carthage students requesting a committee letter
    for applying to medical or dental school
    '''

    # dates
    created_on = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    updated_on = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # owners
    created_by = models.ForeignKey(
        User, verbose_name="Applicant",
        related_name="prehealth_committee_letter_applicant_created_by"
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="prehealth_committee_letter_applicant_updated_by"
    )
    # core
    programs_apply = models.CharField(
        "What Programs are you applying for?",
        choices=PROGRAMS_CHOICES,
        max_length=32
    )
    first_generation = models.CharField(
        "Are you a first generation college student?",
        max_length=4,
        choices=BINARY_CHOICES,
    )
    graduation_date = models.DateField(
        "Expected Graduation Date"
    )
    major = models.CharField(
        "Major(s)",
        max_length=128
    )
    minor = models.CharField(
        "Minor(s)",
        max_length=128
    )
    gpa_overall = models.CharField(
        "Overall GPA", max_length=4,
        validators=[credit_gpa_validator]
    )
    gpa_bcpm = models.CharField(
        "BCPM (Biology, Chemistry, Physics, Math) GPA",
        max_length=4,
        validators=[credit_gpa_validator]
    )
    mcat_dat_scores = models.CharField(
        "MCAT/DAT Scores (if taken)",
        null = True, blank = True,
        max_length=128,
    )
    mcat_dat_date = models.CharField(
        "When will you take the MCAT/DAT again? (if applicable)",
        null = True, blank = True,
        max_length=128
    )
    cv = models.FileField(
        "Résumé",
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text = '''
            Upload a 1-2 page résumé in PDF format.
            The committee will not look at any pages after your second page.
            Your Résumé should be clear and concise. Include areas such as
            awards, scholarships, organizations, work experience,
            volunteer experience, community service, research, etc.
            For health care experiences, you must include hours worked as
            well as length of time (mo/yr to mo/yr). Also include the name
            of your supervisor for any on-campus work.
        '''
    )
    personal_statements = models.FileField(
        upload_to=upload_to_path,
        max_length=768,
        help_text = '''
            <a href="#" target="_blank">
              Please download the Personal Statements form</a>,
            fill it out, scan it or photograph it, and upload it
            above to submit your personal statements and short essays.
        '''
    )
    transcripts = models.FileField(
        upload_to=upload_to_path,
        max_length=768,
        validators=[MimetypeValidator('application/pdf')],
        help_text = '''
            Download your unofficial Carthage transcripts from
            <a href="https://my.carthage.edu/" target="_blank">
                my.carthage.edu</a>
            and save it as a PDF and upload it above.
            The transcripts should include your grades for the fall semester.
        '''
    )
    waiver = models.FileField(
        upload_to=upload_to_path,
        max_length=768,
        help_text = '''
            <a href="#" target="_blank">
                Please download the waiver form</a>,
            fill it out, scan it or photograph it,
            and upload it above. While strongly advised, requesting a
            committee letter through the Carthage Pre-Health Advisory
            Committee is completely optional for medical school or
            dental school applicants. However, in order to apply through
            the committee, we need this waiver signed.
        '''
    )

    @models.permalink
    def get_absolute_url(self):
        return ('prehealth_committee_letter_applicant_detail', [str(self.id)])

    def first_name(self):
        return self.created_by.first_name

    def last_name(self):
        return self.created_by.last_name

    def email(self):
        return self.created_by.email

    def city(self):
        return self.created_by.get_profile().city

    def state(self):
        return self.created_by.get_profile().state

    def phone(self):
        return self.created_by.get_profile().phone

    def get_slug(self):
        return 'pre-health/committee-letter/'


class Recommender(models.Model):
    '''
    Letters of Recommendation
    '''
    user = models.ForeignKey(
        User, verbose_name="Recommender",
        null = True, blank = True,
        related_name="prehealth_recommender"
    )
    name = models.CharField(
        "Name of Recommender",
        max_length=128
    )
    email = models.CharField(
        "Email of Recommender",
        max_length=128
    )

    def get_slug(self):
        return 'pre-health/recommendation/'
