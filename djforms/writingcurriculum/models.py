from django.db import models
from django.contrib.auth.models import User

from djforms.core.models import GenericChoice, BINARY_CHOICES

from djtools.fields.helpers import upload_to_path

DAY_SPS_CHOICES = (
    ('Day', 'Day'),
    ('SPS', 'SPS'),
    ('Both', 'Both'),
)

PERCENT_CHOICES = tuple((str(n), str(n)) for n in range(5,105,5))

class CourseCriteria(models.Model):
    type_assignment = models.CharField(
        max_length=255, null=True, blank=True
    )
    number_pages = models.CharField(
        max_length=3, null=True, blank=True
    )
    percent_grade = models.CharField(
        max_length=3, null=True, blank=True
    )
    description = models.TextField(
        "Description",
        help_text = """
            Describe how you will help students successfully complete
            the assignment, and when during the semester this assignment
            will be addressed.
        """,
        null=True, blank=True
    )

    def __unicode__(self):
        return self.type_assignment

class CourseProposal(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Created by",
        related_name="course_proposal_user",
        editable=False
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="course_proposal_updated_by",
        editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    course_title = models.CharField(
        "Course Title", max_length=128
    )
    course_number = models.CharField(
        "Course number", max_length=16
    )
    department = models.CharField(
        max_length=128
    )
    academic_term = models.ForeignKey(
        GenericChoice,
        related_name="course_proposal_academic_term"
    )
    day_sps = models.CharField(
        verbose_name="Day or SPS",
        max_length=4, choices=DAY_SPS_CHOICES
    )
    approved_wi = models.CharField(
        "Approved WI Course?",
        help_text = """
            This course has been approved by the appropriate
            department as a WI Course.
        """,
        max_length=3, choices=BINARY_CHOICES
    )
    when_approved_wi = models.DateField(
        "If not, when?",
        help_text = """
            If not, when will the course be approved by the department?
        """, null=True, blank=True
    )
    workshop = models.CharField(
        "WI Workshop",
        max_length=3, choices=BINARY_CHOICES,
        help_text = """
            Before an instructor teaches a WI course, he/she must
            have completed a WI workshop. Have you?
        """
    )
    when_workshop = models.DateField(
        "If not, when?",
        null=True, blank=True,
        help_text = """
            If not, when will you complete a WI workshop?
        """
    )
    description = models.TextField("Course Description")
    objectives = models.TextField("Objectives")
    criteria = models.ManyToManyField(
        CourseCriteria,
        related_name="course_proposal_criterion",
        null=True, blank=True
    )
    syllabus = models.FileField(
        upload_to=upload_to_path,
        max_length = "255",
        help_text = """
            If you have a syllabus developed and available in an
            acceptable file format (.doc, .rtf, .pdf), the committee
            would appreciate being able to examine it as well. Use
            the Browse button to find the file on your computer. The
            file (one file, please) will be uploaded when you hit
            Submit below.
        """,
        null=True, blank=True
    )
    learning_outcomes = models.TextField(
        "Three Learning Outcomes",
        help_text = '''
            Please provide three student learning outcomes for writing.
            These outcomes should address the question: how will taking
            this class improve student writing? These outcomes can be
            course/discipline specific. For example, "after completing
            this course, students will be able to define key concepts
            in the field of chemistry in writing" is a clear writing
            outcome. Other examples might include, "after completing
            this course, students will be able to write an analytical
            essay with a clear thesis, and provide adequate support for
            that thesis," or, "after completing this course, students
            will be able to cite in APA style."
        '''
    )
    assessment_methods = models.TextField(
        "Assessment Methods",
        null=True, blank=True,
        help_text = '''
            We assume that your student learning outcomes will be
            assessed through writing assignments. However, if this is
            NOT the case, please describe above how you will assess
            student progress on the learning outcomes you have identified
            (if you leave this field empty, we will assume you are
            assessing through your writing assignments).
        '''
    )
    permission = models.CharField(
        "Archive Permission",
        max_length=3,
        choices=BINARY_CHOICES,
        help_text = """
            Do you grant the WAC Committee permission to add your syllabus
            to our public archive of syllabi for WI courses?
        """
    )

    class Meta:
        ordering = ('-date_created',)
        get_latest_by = 'date_created'

    @models.permalink
    def get_absolute_url(self):
        return ('writing_curriculum_request_detail', [str(self.id)])

    @models.permalink
    def get_update_url(self):
        return ('writing_curriculum_request_update', [str(self.id)])

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def phone(self):
        return self.user.get_profile().phone

    def get_slug(self):
        return "writingcurriculum/"
