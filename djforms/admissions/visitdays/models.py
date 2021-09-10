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
        ).exclude(active=False).order_by('ranking')
    ]
    return {'id__in':ids}


def limit_format():
    ids = [
        g.id for g in GenericChoice.objects.filter(
            tags__name__in=['Admissions Contact Platform'],
        ).exclude(active=False).order_by('ranking')
    ]
    return {'id__in':ids}


class VisitDay(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(
        max_length=255, verbose_name='Slug', unique=True,
    )
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
    extended = models.BooleanField(
        "Extended Form",
        default=False,
        help_text="""
            Check this box if you want the long form with fields for
            Educational Background and Plans
        """,
    )
    number_attend = models.BooleanField(
        "Number Attending",
        default=False,
        help_text="""
            Check this box if you want field with 'Number Attending'.
        """,
    )
    date_alternate = models.BooleanField(
        "Enable an alternate date option",
        default=False,
        help_text="""
            Check this box if you want to allow users to choose
            a alternate date for their visit.
        """,
    )
    time_slots = models.BooleanField(
        "Enable time slots",
        default=False,
        help_text="""
            Check this box if you want to allow users to choose
            time slots for their visit.
        """,
    )
    meeting_format = models.BooleanField(
        "Enable meeting format",
        default=False,
        help_text="""
            Check this box if you want to allow users to choose
            a format for online meeting.
        """,
    )
    meeting_request = models.BooleanField(
        "Enable meeting requests",
        default=False,
        help_text="""
            Check this box if you want to allow users to choose
            meeting requests (e.g. coaches, faculty) for their appointment.
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
    event = models.ForeignKey(VisitDay, on_delete=models.CASCADE)

    def __unicode__(self):
        return "{0} ({1})".format(
            str(self.date.strftime(DATEFORMAT)), self.time,
        )


class VisitDayBaseProfile(GenericContact):
    date = models.ForeignKey(
        VisitDayEvent,
        related_name='visitday_date',
        on_delete=models.CASCADE,
    )
    date_alternate = models.ForeignKey(
        VisitDayEvent,
        related_name='visitday_altdate',
        verbose_name="Second choice date",
        on_delete=models.CASCADE,
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
    number_attend = models.CharField(
        max_length=2,
        verbose_name="Number Attending",
        null=True,
        blank=True,
    )
    time_primary = models.ForeignKey(
        GenericChoice,
        verbose_name="Time, First Choice",
        related_name='visit_day_time_primary',
        limit_choices_to=limit_time,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    time_secondary = models.ForeignKey(
        GenericChoice,
        verbose_name="Time, Second Choice",
        related_name='visit_day_time_secondary',
        limit_choices_to=limit_time,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    meeting_format = models.ForeignKey(
        GenericChoice,
        verbose_name="Meeting Format",
        related_name='visit_day_format',
        limit_choices_to=limit_format,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    meeting_request = models.ManyToManyField(
        GenericChoice,
        verbose_name="Meeting Requests",
        related_name="visit_day_request",
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
        "High School city", max_length=128
    )
    hs_state = USStateField("High School state")
    hs_grad_year = models.IntegerField("High School graduation year")
    entry_as = models.CharField(
        "Entering as a", max_length=16, choices=ENTRY_CHOICES
    )
    transfer = models.CharField(
        "If transfer, list university/college attended and city/state",
        max_length=255, null=True, blank=True
    )
    entry_year = models.IntegerField("Entry year")
    entry_term = models.CharField(
        "Entry term", max_length=32, choices=SEMESTER_CHOICES
    )
    academic = models.TextField(
        "Academic interests", null=True, blank=True
    )
    xtracurricular = models.TextField(
        "Extracurricular interests (clubs, fine arts, sports, etc.)",
        null=True, blank=True
    )
    comments = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return u'{0} {1}'.format(self.last_name, self.first_name)

    def event_title(self):
        return self.date.event.title
