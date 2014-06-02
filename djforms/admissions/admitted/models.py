from django.db import models

STATUS = (
    ("Freshman","Freshman"),
    ("Transfer","Transfer"),
)

GPA_SCALE = (
    ("4.0","4.0"),
    ("5.0","5.0"),
    ("6.0","6.0"),
    ("7.0","7.0"),
    ("8.0","8.0"),
    ("9.0","9.0"),
    ("10.0","10.0"),
    ("11.0","11.0"),
    ("12.0","12.0"),
    ("100","100"),
)

class Candidate(models.Model):
    # dates
    created_on = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    updated_on = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    # core
    first_name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128)
    status = models.CharField(
        max_length=12,
        choices=STATUS,
        default="Freshman"
    )
    act_sat = models.CharField(
        "ACT or SAT",
        max_length=12,
        help_text="(SAT=Critical Reading + Math)"
    )
    gpa = models.CharField(
        "GPA", max_length=4
    )
    gpa_scale = models.CharField(
        "GPA Scale",
        max_length=4,
        choices=GPA_SCALE
    )
    adjusted_gpa = models.CharField(max_length=8)
    information = models.TextField(
        "Aditional Information",
        help_text="i.e. extracurriculars, AP, etc.",
        blank=True, null=True
    )
    prospect_status = models.CharField(
        max_length=64, blank=True, null=True
    )

    class Meta:
        app_label = 'admissions'
        verbose_name_plural = "Will I be admitted?"

    def __unicode__(self):
        return u'%s <%s>' % (self.first_name, self.email)

