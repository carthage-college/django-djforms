from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from djforms.core.models import BINARY_CHOICES
from djforms.core.models import GenericContact

from localflavor.us.models import USStateField

class PhageHunter(GenericContact):
    #core
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=128)
    state = USStateField()
    postal_code = models.CharField(max_length=10, verbose_name = 'Zip code')
    phone = models.CharField(
        'Telephone', max_length=12, help_text="Format: XXX-XXX-XXXX"
    )
    # high school and academics
    high_school = models.CharField("High School", max_length=255)
    gpa = models.CharField("Cumulative GPA", max_length=4)
    act_comp = models.CharField(
        "ACT Composite", max_length=2, null=True, blank=True
    )
    act_math = models.CharField(
        "ACT Math", max_length=2, null=True, blank=True
    )
    act_science = models.CharField(
        "ACT Science Reasoning", max_length=2, null=True, blank=True
    )
    sat_comp = models.CharField(
        "SAT Composite", max_length=4, null=True, blank=True
    )
    sat_math = models.CharField(
        "SAT Math", max_length=3, null=True, blank=True
    )
    sat_read = models.CharField(
        "SAT Critical Reading", max_length=3, null=True, blank=True
    )
    intended_majors = models.CharField(max_length=255)
    high_school_science = models.TextField(
        max_length=128,
        help_text="""
            Please list all high school science courses
            that you have completed.
        """
    )
    biology_chemistry_courses = models.TextField(
        "Biology/Chemistry Courses",
        help_text="""
            Please describe the biology and/or chemistry
            courses you have taken.
        """
    )
    research_experience = models.TextField(
        help_text="Please describe any research experience."
    )
    program_interest = models.TextField(
        help_text='Please describe why you are interested in the program.'
    )
    lab_work = models.CharField(
        max_length=3, choices=BINARY_CHOICES,
        help_text="Are you willing to spend extra time in the lab as needed?"
    )

    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return "http://%s%s" % (
            settings.SERVER_URL,
            reverse("phage_hunters_detail", args=[self.pk])
    )
