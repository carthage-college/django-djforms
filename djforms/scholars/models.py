# -*- coding: utf-8 -*-

import json
import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from djforms.core.models import BINARY_CHOICES
from djforms.core.models import Department
from djforms.core.models import YEAR_CHOICES
from djtools.fields import NOW
from djtools.fields.validators import MimetypeValidator
from djtools.utils.mail import send_mail
from taggit.managers import TaggableManager


FILE_VALIDATORS = [MimetypeValidator('image/png')]
WORK_TYPES = (
    ('SURE', 'SURE'),
    ('Senior thesis', 'Senior thesis'),
    ('Independent research', 'Independent research'),
    ('Course project', 'Course project'),
    ("Master's thesis", "Master's thesis"),
)
PRESENTER_TYPES = (
    ('', '----select----'),
    ('Student', 'Student'),
    ('Faculty', 'Faculty'),
    ('Staff', 'Staff'),
)
YEAR = NOW.year


class Person(object):
    """
    Dynamic 'person' object.

    Usage:

    data = {"name":"larry","email":"larry@carthage.edu"}
    p = Person(**data)
    p.id = 90125
    etc
    """

    def __init__(self, **entries):
        """Initialization method."""
        self.__dict__.update(entries)


def get_json(yuri):
    """Obtain the json data from directory API."""
    jason = cache.get('{0}_api_json'.format(yuri))
    if jason is None:
        # read the json data from URL
        earl = "{0}{1}/screen/?api_key={2}".format(
            settings.API_PEOPLE_URL, yuri, settings.API_KEY,
        )
        response =  requests.get(earl)
         #jason_data = json.loads(response.text)
        #data = response.read()
        # json doesn't like trailing commas, so...
        #data = data.replace(',]', ']')
        data = response.text
        jason = json.loads(response.text)
        cache.set('{0}_api_json'.format(yuri), jason)
    return jason


def get_people(yuri):
    """Obtain the group of people from the directory API."""
    people = cache.get('{0}_api_objects'.format(yuri))
    if people is None:
        jason = get_json(yuri)
        people = {}
        for jay in jason:
            person = Person(**jay)
            people[person.id] = person
        cache.set('{0}_api_objects'.format(yuri), people)
    return people


class Presenter(models.Model):
    """Data model class for the presenter."""

    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    date_updated = models.DateTimeField("Date Updated", auto_now=True)
    college_id = models.CharField(max_length=8, null=True, blank=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    leader = models.BooleanField("Presentation leader", default=False)
    prez_type = models.CharField(
        "Presenter type",
        max_length=16,
        choices=PRESENTER_TYPES,
        null=True,
        blank=True,
    )
    college_year = models.CharField(
        "Current year at Carthage",
        max_length=1,
        choices=YEAR_CHOICES,
        null=True,
        blank=True,
    )
    major = models.CharField(max_length=128, null=True, blank=True)
    hometown = models.CharField(max_length=128, null=True, blank=True)
    sponsor = models.CharField(max_length=128, null=True, blank=True)
    sponsor_name = models.CharField(max_length=128, null=True, blank=True)
    sponsor_email = models.CharField(max_length=128, null=True, blank=True)
    sponsor_other = models.CharField(max_length=255, null=True, blank=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    mugshot = models.ImageField(
        max_length=255,
        upload_to="files/scholars/mugshots",
        help_text="75 dpi and .jpg only",
    )
    ranking = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        """Default value for the objects."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        """Override the save() method to update some things first."""
        if self.sponsor:
            faculty = get_people("faculty")
            try:
                self.sponsor_name = '{0} {1}'.format(
                    faculty[self.sponsor].firstname,
                    faculty[self.sponsor].lastname,
                )
                self.sponsor_email = faculty[self.sponsor].email
            except Exception:
                self.sponsor_name = settings.COS_DEFAULT_NAME
                self.sponsor_email = settings.COS_DEFAULT_EMAIL
        super(Presenter, self).save()

    def year(self):
        """Deal with academic years."""
        if self.college_year:
            year = YEAR_CHOICES[int(self.college_year)][1]
        else:
            year = None
        return year

    def presenter_type(self):
        """Display the presenter type."""
        return PRESENTOR_TYPES[self.prez_type][1]


class Presentation(models.Model):
    """Data model class for the presentation."""

    user = models.ForeignKey(
        User,
        verbose_name="Created by",
        related_name='presentation_created_by',
        on_delete=models.CASCADE,
    )
    updated_by = models.ForeignKey(
        User,
        verbose_name="Updated by",
        related_name='presentation_updated_by',
        editable=False,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField("Date Created", auto_now_add=True)
    date_updated = models.DateTimeField("Date Updated", auto_now=True)
    tags = TaggableManager()
    ranking = models.IntegerField(null=True, blank=True, default=0)
    title = models.CharField("Presentation title", max_length=255)
    reviewer = models.CharField(max_length=128, null=True, blank=True)
    leader = models.ForeignKey(
        Presenter,
        verbose_name="Presentation leader",
        related_name='presentation_leader',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    presenters = models.ManyToManyField(
        Presenter, related_name="presentation_presenters", blank=True,
    )
    funding = models.CharField(
        "Funding source (if applicable)",
        max_length=255,
        help_text="e.g. external funding, SURE, etc.",
        null=True,
        blank=True,
    )
    work_type = models.CharField(max_length=32, choices=WORK_TYPES)
    permission = models.CharField(
        "Permission to reproduce",
        max_length=3,
        choices=BINARY_CHOICES,
        help_text="""
            Do you grant Carthage permission to reproduce your presentation?
        """,
    )
    shared = models.CharField(
        "Faculty sponsor approval",
        max_length=3,
        choices=BINARY_CHOICES,
        help_text="""
            Has your faculty sponsor approved your proposal?
            Note: Faculty and staff presenters should choose 'yes'.
        """,
    )
    abstract_text = models.TextField(
        "Abstract",
        help_text="Copy and paste your abstract text or start typing.",
    )
    need_table = models.CharField(max_length=3, choices=BINARY_CHOICES)
    need_electricity = models.CharField(max_length=3, choices=BINARY_CHOICES)
    poster_file = models.FileField(
        upload_to='files/scholars/posters/{0}'.format(YEAR),
        validators=FILE_VALIDATORS,
        help_text="Upload a poster file",
        null=True,
        blank=True,
    )
    status = models.BooleanField(default=False)

    class Meta:
        """Sub-class for settings configurations about the parent class."""

        ordering = ['date_created']
        get_latest_by = 'date_created'
        permissions = (('manage_presentation', 'manage presentation'))

    def __str__(self):
        """Display the default value."""
        return self.title

    def save(self, *args, **kwargs):
        """Override the save() method to update some things first."""
        # send email if approved
        if self.pk is not None:
            prez = Presentation.objects.get(pk=self.pk)
            if (prez.status != self.status) and self.status:
                if settings.DEBUG:
                    TO_LIST = [settings.SERVER_EMAIL]
                else:
                    TO_LIST = [self.user.email,]
                BCC = settings.MANAGERS
                email = settings.DEFAULT_FROM_EMAIL
                subject = '[Celebration of Scholars] Presentation has been approved'
                send_mail(
                    None,
                    TO_LIST,
                    subject,
                    email,
                    'scholars/presentation/approved_mail.html',
                    self,
                    BCC,
                )
        else:
            self.updated_by = self.user
        super(Presentation, self).save()

    def tag_list(self):
        """Display the tags for the presentation."""
        return ', '.join(tag.name for tag in self.tags.all())

    def get_absolute_url(self):
        """Return the default URL."""
        return reverse('presentation_detail', kwargs={'pid': self.id})

    def get_update_url(self):
        """Return the update URL."""
        return reverse('presentation_update', kwargs={'pid': self.id})

    def get_presenters(self):
        """Obtain all presenters for this presentation."""
        return self.presenters.order_by('-leader', 'last_name')

    def get_presenters_print(self):
        """Obtain all presenters for print."""
        return self.presenters.order_by('last_name')

    def mugshot_status(self):
        """Return the status if all the presenters have a mugshot or not."""
        status = True
        for presenter in self.presenters.all():
            if not presenter.mugshot:
                status = False
                break
        return status

    def first_name(self):
        """Display the user's given name."""
        return self.user.first_name

    def last_name(self):
        """Display the user's sur name."""
        return self.user.last_name

    def email(self):
        """Display the user's email."""
        return self.user.email

    def sponsor(self):
        """Return the leader's sponsor email."""
        if self.leader:
            return self.leader.sponsor_email
        else:
            return None

    def sponsor_other(self):
        """Return the leader's sponsor."""
        if self.leader:
            return self.leader.sponsor_other
        else:
            return None

    def poster(self):
        """Return all of the posters."""
        poster = False
        if self.poster_file:
            poster = mark_safe(
                '<a href="https://{0}/assets/{1}">Download</a>'.format(
                    settings.SERVER_URL, self.poster_file,
                ),
            )
        return poster
    poster.allow_tags = True

    def presentation_type(self):
        """Return the presentation type."""
        return WORK_TYPES[self.work_type][1]
