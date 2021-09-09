# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from djforms.core.models import GenericChoice

from djtools.fields import BINARY_CHOICES
from djtools.fields.helpers import upload_to_path
from djtools.fields.validators import MimetypeValidator
from djtools.fields.validators import credit_gpa_validator

RANKING_CHOICES = (
    ('Outstanding','Outstanding'),
    ('Excellent','Excellent'),
    ('Above Average','Above Average'),
    ('Average','Average'),
    ('Fair','Fair'),
    ('Poor','Poor'),
    ('No basis to evaluate','No basis to evaluate'),
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
        related_name='prehealth_committee_letter_applicant_created_by',
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name='prehealth_committee_letter_applicant_updated_by',
        on_delete=models.CASCADE,
    )
    # core
    programs_apply = models.ManyToManyField(
        GenericChoice, verbose_name="For which programs are you applying?",
        related_name='prehealth_committee_letter_applicant_programs'
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
        null = True, blank = True,
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
    mcat_dat_date = models.DateField(
        "When will you take the MCAT/DAT again? (if applicable)",
        null = True, blank = True,
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
            <a href="https://www.carthage.edu/live/files/3254" target="_blank">
              Please download the Personal Statements form</a>,
            complete the form, and upload it
            above to submit your personal statements and short essays.
            Please make sure your document is a PDF and contains your name
            and the date.
        '''
    )
    core_competencies = models.FileField(
        upload_to=upload_to_path,
        max_length=768,
        validators=[MimetypeValidator('application/pdf')],
        help_text = '''
            <a href="https://www.aamc.org/services/admissions-lifecycle/competencies-entering-medical-students" target="_blank">
            View the list of the AAMC Core competencies</a>.
            On a PDF document that you upload below, list the three core
            competencies that you most excel in with a short paragraph
            explaining why you chose each competency
            (150 word maximum per competency).
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
        validators=[MimetypeValidator('application/pdf')],
        help_text = '''
            <a href="/live/files/3255" target="_blank">
            Please download the waiver form</a>.
            Fill it out, scan it, and upload it as
            a PDF it below. While strongly advised, requesting a committee letter
            through the Carthage Pre-Health Advisory Committee is completely optional
            for medical school or dental school applicants. However, in order to apply
            through the committee, we need this waiver signed (not typed).
        '''
    )

    def get_absolute_url(self):
        return reverse(
            'prehealth_committee_letter_applicant_detail',
            args=(str(self.id)),
        )

    def first_name(self):
        return self.created_by.first_name

    def last_name(self):
        return self.created_by.last_name

    def email(self):
        return self.created_by.email

    def city(self):
        return self.created_by.userprofile.city

    def state(self):
        return self.created_by.userprofile.state

    def phone(self):
        return self.created_by.userprofile.phone

    def get_slug(self):
        return 'pre-health/committee-letter/'

    def __unicode__(self):
        return u'{}, {}'.format(
            self.created_by.last_name, self.created_by.first_name
        )


class Recommendation(models.Model):
    '''
    Letters of Recommendation
    '''

    applicant = models.ForeignKey(
        Applicant, verbose_name="Applicant",
        related_name='prehealth_committee_letter_recommendation_applicant',
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        "Name of Recommender",
        max_length=128
    )
    email = models.CharField(
        "Email of Recommender",
        max_length=128
    )


class Evaluation(models.Model):
    '''
    Evanluation form
    '''

    created_by = models.ForeignKey(
        User, verbose_name="Applicant",
        related_name='prehealth_committee_letter_evaluation_created_by',
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name='prehealth_committee_letter_evaluation_updated_by',
        on_delete=models.CASCADE,
    )
    applicant = models.ForeignKey(
        Applicant, verbose_name="Applicant",
        related_name='prehealth_committee_letter_evaluation_applicant',
        on_delete=models.CASCADE,
    )
    knowledge = models.CharField(
        "Knowledge of Subject Matter",
        max_length=64,
        choices=RANKING_CHOICES,
    )
    curiosity = models.CharField(
        "Intellectual Curiosity",
        max_length=64,
        choices=RANKING_CHOICES,
    )
    communication = models.CharField(
        "Communication Skills – Oral/Written",
        max_length=64,
        choices=RANKING_CHOICES,
    )
    cooperation = models.CharField(
        "Ability to get along with Others – Willingness to Cooperate",
        max_length=64,
        choices=RANKING_CHOICES,
    )
    maturity = models.CharField(
        "Maturity",
        max_length=64,
        choices=RANKING_CHOICES,
    )
    integrity = models.CharField(
        "Integrity",
        max_length=64,
        choices=RANKING_CHOICES,
    )
    overall = models.CharField(
        "Overall Evaluation",
        max_length=64,
        choices=RANKING_CHOICES,
    )
    recommendation = models.FileField(
        upload_to=upload_to_path,
        validators=[MimetypeValidator('application/pdf')],
        max_length=768,
        help_text = '''
            Upload your letter of recommendation in PDF format.
        '''
    )

    def get_slug(self):
        return 'pre-health/committee-letter/evaluation/'

