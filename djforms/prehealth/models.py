# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from djtools.fields import BINARY_CHOICES
from djtools.fields.helpers import upload_to_path
from djtools.fields.validators import credit_gpa_validator

PROGRAMS_CHOICES = (
    ("M.D.","M.D"),
    ("D.O.","D.O."),
    ("D.D.S.","D.D.S."),
    ("M.D./Ph.D.","M.D./Ph.D")
)


class CommitteeLetter(models.Model):
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
    # core
    user = models.ForeignKey(
        User, verbose_name="Created by",
        related_name="applicant_created_by"
    )
    programs_apply = models.CharField(
        "What Programs are you applying for?",
        choices=PROGRAMS_CHOICES,
        max_length="32"
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
        max_length=768,
        help_text = '''
            Upload a 1-2 page typed resume by March 3rd, 2017.
            The committee will not look at any pages after your second page.
            Your Resume should be clear and concise. Include areas such as
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
            Download the following form to submit your
            personal statements and short essays
        '''
    )
    transcripts = models.FileField(
        upload_to=upload_to_path,
        max_length=768,
        help_text = '''
            Download your unofficial Carthage transcripts from
            <a href="https://my.carthage.edu/" target="_blank">my.carthage.edu</a>
            and save it as a pdf and upload it above.
            The transcripts should include your grades for the fall semester.
        '''
    )
    waiver = models.FileField(
        upload_to=upload_to_path,
        max_length=768,
        help_text = '''
            <a href="#" target="_blank">
                Please download the waiver form</a>.
            Fill it out, scan it,
            and upload it above. While strongly advised, requesting a
            committee letter through the Carthage Pre-Health Advisory
            Committee is completely optional for medical school or
            dental school applicants. However, in order to apply through
            the committee, we need this waiver signed.
        '''
    )

    def get_slug(self):
        return "pre-health/committee-letter/"
    )

    '''
    def get_slug(self):
        return "pre-health/recommendation/"
    )
    '''
