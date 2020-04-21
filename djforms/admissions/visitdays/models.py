from django.db import models

from djforms.core.models import GENDER_CHOICES
from djforms.core.models import GenericChoice
from djforms.core.models import GenericContact
from djforms.core.models import SEMESTER_CHOICES

from localflavor.us.models import USStateField

ENTRY_CHOICES = [
    ('Freshman','Freshman'),
    ('Transfer','Transfer'),
]
GUARDIAN_CHOICES = (
    ('Mother', 'Mother'),
    ('Father', 'Father'),
    ('Guardian', 'Guardian'),
)
DATEFORMAT = '%A, %B %d, %Y'

def limit_time():
    ids = [
        g.id for g in GenericChoice.objects.filter(
            tags__name__in=['Admissions Visit Time'],
        ).order_by('ranking')
    ]
    return {'id__in':ids}


def limit_format():
    ids = [
        g.id for g in GenericChoice.objects.filter(
            tags__name__in=['Admissions Contact Platform'],
        ).order_by('ranking')
    ]
    return {'id__in':ids}


class VisitDay(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(
        "Description",
        help_text="This information will appear above the form.",
    )
    about = models.TextField(
        "About",
        help_text="""
            This information will appear in the sidebar next to the form.
        """,
    )
    email_info = models.TextField(
        "Email Instructions",
        help_text="This information will be sent to the registrant.",
        null=True,
        blank=True,
    )
    slug = models.CharField(
        max_length=255, verbose_name='Slug', unique=True,
    )
    extended = models.BooleanField(
        "Extended Form",
        default=False,
        help_text="""
            Check this box if you want the long form with fields for
            Educational Background and Plans
        """,
    )
    date_alternate = models.BooleanField(
        "Enable an alternate date option",
        default=False,
        help_text="""
            Check this box if you want to allow users to
            choose a alternate date for their visit.
        """,
    )
    time_slots = models.BooleanField(
        "Enable time slots",
        default=False,
        help_text="""
            Check this box if you want to allow users to
            choose time slots for their visit.
        """,
    )
    meeting_format = models.BooleanField(
        "Enable meeting format",
        default=False,
        help_text="""
            Check this box if you want to allow users to
            choose a format for online meeting.
        """,
    )

    def __unicode__(self):
        return self.title


class VisitDayEvent(models.Model):
    date = models.DateField()
    time = models.CharField(
        help_text="Morning or Afternoon or time frame (e.g. 6-8pm)",
        max_length=32,
    )
    max_attendees = models.IntegerField()
    cur_attendees = models.IntegerField()
    active = models.BooleanField(default=True)
    event = models.ForeignKey(VisitDay)

    def __unicode__(self):
        return "{0} ({1})".format(
            str(self.date.strftime(DATEFORMAT)), self.time,
        )


class VisitDayBaseProfile(GenericContact):
    date = models.ForeignKey(VisitDayEvent, related_name='visitday_date')
    date_alternate = models.ForeignKey(
        VisitDayEvent,
        related_name='visitday_altdate',
        verbose_name="Second choice date",
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=255, verbose_name="Address")
    city = models.CharField(max_length=128, verbose_name="City")
    state = USStateField()
    postal_code = models.CharField(max_length=10, verbose_name="Zip Code")
    phone = models.CharField(
        max_length=12,
        verbose_name="Phone Number",
        help_text="Format: XXX-XXX-XXXX",
    )
    mobile = models.CharField(
        max_length=12,
        verbose_name="Mobile Phone",
        help_text="Format: XXX-XXX-XXXX",
        null=True,
        blank=True,
    )
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES)
    number_attend = models.IntegerField(verbose_name = "Number Attending")
    time_primary = models.ForeignKey(
        GenericChoice,
        verbose_name="Time, First Choice",
        related_name='visit_day_time_primary',
        limit_choices_to=limit_time,
        null=True,
        blank=True,
    )
    time_secondary = models.ForeignKey(
        GenericChoice,
        verbose_name="Time, Second Choice",
        related_name='visit_day_time_secondary',
        limit_choices_to=limit_time,
        null=True,
        blank=True,
    )
    meeting_format = models.ForeignKey(
        GenericChoice,
        verbose_name="Meeting Format",
        related_name='visit_day_format',
        limit_choices_to=limit_format,
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return u'{0} {1}'.format(self.last_name, self.first_name)


class VisitDayProfile(VisitDayBaseProfile):
    guardian_email = models.EmailField(null=True, blank=True)
    guardian_type = models.CharField(
        "Parent/Guardian type", max_length=16, choices=GUARDIAN_CHOICES
    )
    high_school = models.CharField(
        "High School", max_length=255
    )
    hs_city = models.CharField(
        "High School City", max_length=128
    )
    hs_state = USStateField("High School State")
    hs_grad_year = models.IntegerField("High School Graduation Year")
    entry_as = models.CharField(
        "Entering as a", max_length=16, choices=ENTRY_CHOICES
    )
    transfer = models.CharField(
        "If transfer, list University/College Attended and City/State",
        max_length=255, null=True, blank=True
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
        return u'{0} {1}'.format(self.last_name, self.first_name)

    def event_title(self):
        return self.date.event.title
