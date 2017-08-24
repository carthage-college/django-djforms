from django.db import models

from djforms.core.models import GenericContact,GENDER_CHOICES,SEMESTER_CHOICES

from localflavor.us.models import USStateField

ENTRY_CHOICES = [
    ('Freshman','Freshman'),
    ('Transfer','Transfer'),
]

DATEFORMAT = '%A, %B %d, %Y'


class VisitDay(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(
        "Description",
        help_text="This information will appear above the form."
    )
    about = models.TextField(
        "About",
        help_text="""
            This information will appear in the sidebar next to the form.
        """
    )
    email_info = models.TextField(
        "Email Instructions",
        help_text="This information will be sent to the registrant."
    )
    slug = models.CharField(
        max_length=255, verbose_name="Slug", unique=True
    )
    extended = models.BooleanField(
        "Extended Form",
        default=False,
        help_text="""
            Check this box if you want the long form with fields for
            Educational Background and Plans
        """
    )

    def __unicode__(self):
        return self.title


class VisitDayEvent(models.Model):
    date = models.DateField()
    time = models.CharField(
        help_text="Morning or Afternoon or time frame (e.g. 6-8pm)",
        max_length=32
    )
    max_attendees = models.IntegerField()
    cur_attendees = models.IntegerField()
    active = models.BooleanField(default=True)
    event = models.ForeignKey(VisitDay)

    def __unicode__(self):
        return "{} ({})".format(str(self.date.strftime(DATEFORMAT)), self.time)


class VisitDayBaseProfile(GenericContact):
    date = models.ForeignKey(VisitDayEvent)
    address = models.CharField(
        max_length=255, verbose_name = 'Address')
    city = models.CharField(
        max_length=128, verbose_name = 'City'
    )
    state = USStateField()
    postal_code = models.CharField(
        max_length=10, verbose_name = 'Zip Code'
    )
    phone = models.CharField(
        max_length=12, verbose_name='Phone Number',
        help_text="Format: XXX-XXX-XXXX"
    )
    mobile = models.CharField(
        max_length=12, verbose_name='Mobile Phone',
        help_text="Format: XXX-XXX-XXXX",
        null=True, blank=True
    )
    gender = models.CharField(
        max_length=16, choices=GENDER_CHOICES
    )
    number_attend = models.IntegerField(
        verbose_name = "Number Attending"
    )

    def __unicode__(self):
        return u'{} {}'.format(self.last_name, self.first_name)


class VisitDayProfile(VisitDayBaseProfile):
    high_school = models.CharField(
        "High School", max_length=255
    )
    hs_city = models.CharField(
        "High School City", max_length=128
    )
    hs_state = USStateField("High School State")
    hs_grad_year = models.IntegerField("High School Graduation Year")
    entry_as = models.CharField(
        "Entering as a", max_length="16", choices=ENTRY_CHOICES
    )
    transfer = models.CharField(
        "If transfer, list University/College Attended and City/State",
        max_length="255", null=True, blank=True
    )
    entry_year = models.IntegerField("Entry Year")
    entry_term = models.CharField(
        "Entry Term", max_length=32, choices=SEMESTER_CHOICES
    )
    academic = models.TextField(
        "Academic Interests", null=True, blank=True
    )
    xtracurricular = models.TextField(
        "Extracurricular Interests (clubs, fine arts, sports, etc.)",
        null=True, blank=True
    )
    comments = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'{} {}'.format(self.last_name, self.first_name)

