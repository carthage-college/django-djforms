from django.db import models
from django.core.urlresolvers import reverse
from djforms.core.models import BINARY_CHOICES, GENDER_CHOICES

from django.contrib.localflavor.us.models import USStateField

from djforms.core.models import GenericContact

class PhageHunter(GenericContact):
    # dates
    created_on  = models.DateTimeField("Date Created", auto_now_add=True)
    updated_on  = models.DateTimeField("Date Updated", auto_now=True)
    #core
    address         = models.CharField(max_length=255)
    city            = models.CharField(max_length=128)
    state           = USStateField()
    postal_code     = models.CharField(max_length=10, verbose_name = 'Zip code')
    phone           = models.CharField('Telephone', max_length=12, help_text="Format: XXX-XXX-XXXX")
    gender          = models.CharField(max_length="16", choices=GENDER_CHOICES)
    # high school and academics
    high_school                 = models.CharField("High School", max_length=255)
    gpa                         = models.CharField("Cumulative GPA", max_length=4)
    act                         = models.CharField("ACT", max_length=2)
    act_math                    = models.CharField("ACT math", max_length=2)
    act_science                 = models.CharField("ACT science", max_length=2)
    intended_majors             = models.CharField(max_length=128, null=True, blank=True)
    intended_majors_other       = models.CharField("Other", max_length=128, null=True, blank=True)
    high_school_science         = models.TextField(max_length=128, help_text="Please list all high school science courses that you have completed.")
    biology_chemistry_courses   = models.TextField("Biology/Chemistry Courses", help_text="Please describe the biology and/or chemistry courses you have taken.")
    research_experience         = models.TextField(help_text="Please describe any research experience.")
    program_interest            = models.TextField(help_text='Please describe why you are interested in the program.')
    lab_work                    = models.CharField(max_length=3, choices=BINARY_CHOICES, help_text="Are you willing to spend extra time in the lab as needed?")

    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)

    def get_absolute_url(self):
        return reverse("phage_hunter_detail", args=[self.pk])

    def majors(self):
        return eval(self.intended_majors)
