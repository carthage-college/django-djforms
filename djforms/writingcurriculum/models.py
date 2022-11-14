# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from djforms.core.models import BINARY_CHOICES
from djforms.core.models import GenericChoice
from djtools.fields.helpers import upload_to_path
from djtools.templatetags.livewhale_api import get_api_data


DAY_SPS_CHOICES = (
    ('Day', 'Day'),
    ('SPS', 'SPS'),
    ('Both', 'Both'),
)
PERCENT_CHOICES = tuple((str(n), str(n)) for n in range(5,105,5))


class CourseCriteria(models.Model):

    type_assignment = models.CharField(max_length=255, null=True, blank=True)
    number_pages = models.CharField(max_length=3, null=True, blank=True)
    percent_grade = models.CharField(max_length=3, null=True, blank=True)
    description = models.TextField(
        "Description",
        help_text="""
            Describe how you will help students successfully complete
            the assignment, and when during the semester this assignment
            will be addressed.
        """,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.type_assignment


class CourseProposal(models.Model):

    user = models.ForeignKey(
        User, verbose_name="Created by",
        related_name='course_proposal_user',
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name='course_proposal_updated_by',
        editable=False,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    date_updated = models.DateTimeField("Date Updated", auto_now=True)
    course_title = models.CharField("Course Title", max_length=128)
    course_number = models.CharField("Course number", max_length=16)
    department = models.CharField(max_length=128)
    academic_term = models.ForeignKey(
        GenericChoice,
        related_name='course_proposal_academic_term',
        on_delete=models.CASCADE,
    )
    day_sps = models.CharField(
        verbose_name="Day or SPS",
        max_length=4,
        choices=DAY_SPS_CHOICES,
    )
    approved_wi = models.CharField(
        "Approved WI Course?",
        help_text="""
            This course has been approved by the appropriate
            department as a WI Course.
        """,
        max_length=3,
        choices=BINARY_CHOICES,
    )
    when_approved_wi = models.DateField(
        "If not, when?",
        help_text="""
            If not, when will the course be approved by the department?
        """,
        null=True,
        blank=True,
    )
    workshop = models.CharField(
        "WI Workshop",
        max_length=3,
        choices=BINARY_CHOICES,
        help_text="""
            Before an instructor teaches a WI course, he/she must
            have completed a WI workshop. Have you?
        """,
    )
    when_workshop = models.DateField(
        "If not, when?",
        help_text = """
            If not, when will you complete a WI workshop?
        """,
        null=True,
        blank=True,
    )
    description = models.TextField("Course Description")
    objectives = models.TextField("Objectives")
    criteria = models.ManyToManyField(
        CourseCriteria,
        related_name="course_proposal_criterion",
    )
    syllabus = models.FileField(
        upload_to=upload_to_path,
        max_length=255,
        help_text=get_api_data(3571)['body'],
        null=True,
        blank=True,
    )
    learning_outcomes = models.TextField(
        "Three Learning Outcomes",
        help_text=get_api_data(3565)['body'],
    )
    assessment_methods = models.TextField(
        "Assessment Methods",
        help_text=get_api_data(3566)['body'],
        null=True,
        blank=True,
    )
    permission = models.CharField(
        "Archive Permission",
        max_length=3,
        choices=BINARY_CHOICES,
        help_text="""
            Do you grant the WAC Committee permission to add your syllabus
            to our public archive of syllabi for WI courses?
        """,
    )

    class Meta:

        ordering = ('-date_created',)
        get_latest_by = 'date_created'

    def get_absolute_url(self):
        return reverse(
            'writing_curriculum_request_update',
            kwargs={'pid': self.id},
        )

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def phone(self):
        return self.user.userprofile.phone

    def get_slug(self):
        return "writingcurriculum/"
