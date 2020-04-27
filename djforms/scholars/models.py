# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from djforms.core.models import Department
from djforms.core.models import YEAR_CHOICES, BINARY_CHOICES
from djtools.fields.validators import MimetypeValidator
from djtools.utils.mail import send_mail
from djtools.fields import NOW

from taggit.managers import TaggableManager

import urllib, json

FILE_VALIDATORS = [MimetypeValidator('application/pdf')]
#FILE_VALIDATORS = []

WORK_TYPES = (
    #('','----select----'),
    ('SURE','SURE'),
    ('Senior thesis','Senior thesis'),
    ('Independent research','Independent research'),
    ('Course project','Course project'),
    ("Master's thesis","Master's thesis")
)
PRESENTER_TYPES = (
    ('','----select----'),
    ('Student','Student'),
    ('Faculty','Faculty'),
    ('Staff','Staff'),
)
YEAR = NOW.year


class Person(object):
    """
    Dynamic 'person' object
    Usage:

    data = {"name":"larry","email":"larry@carthage.edu"}
    p = Person(**data)
    p.id = 90125
    etc
    """
    def __init__(self, **entries):
        self.__dict__.update(entries)

def get_json(yuri):
    jason = cache.get('%s_api_json' % yuri)
    if jason is None:
        # read the json data from URL
        earl = "%s/%s/?api_key=%s" % (
            settings.API_PEOPLE_URL,yuri,settings.API_KEY
        )
        response =  urllib.urlopen(earl)
        data = response.read()
        # json doesn't like trailing commas, so...
        data = data.replace(',]',']')
        jason = json.loads(data)
        cache.set('%s_api_json' % yuri, jason)
    return jason

def get_people(yuri):
    people = cache.get('%s_api_objects' % yuri)
    if people is None:
        jason = get_json(yuri)
        people = {}
        for j in jason:
            p = Person(**j)
            people[p.id] = p
        cache.set('%s_api_objects' % yuri, people)
    return people

class Presenter(models.Model):
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    college_id = models.CharField(
        max_length=8, null=True, blank=True
    )
    first_name = models.CharField(
        max_length=128, null=True, blank=True
    )
    last_name = models.CharField(
        max_length=128, null=True, blank=True
    )
    email = models.CharField(
        max_length=128, null=True, blank=True
    )
    leader = models.BooleanField(
        "Presentation leader", default=False
    )
    prez_type = models.CharField(
        "Presenter type", max_length=16,
        choices=PRESENTER_TYPES, null=True, blank=True
    )
    college_year = models.CharField(
        "Current year at Carthage", max_length=1,
        choices=YEAR_CHOICES, null=True, blank=True
    )
    major = models.CharField(
        max_length=128, null=True, blank=True
    )
    hometown = models.CharField(
        max_length=128, null=True, blank=True
    )
    sponsor = models.CharField(
        max_length=128, null=True, blank=True
    )
    sponsor_name = models.CharField(
        max_length=128, null=True, blank=True
    )
    sponsor_email = models.CharField(
        max_length=128, null=True, blank=True
    )
    sponsor_other = models.CharField(
        max_length=255, null=True, blank=True
    )
    department = models.ForeignKey(
        Department, null=True, blank=True
    )
    mugshot = models.ImageField(
        max_length=255, upload_to="files/scholars/mugshots",
        help_text="75 dpi and .jpg only"
    )
    ranking = models.IntegerField(
        null=True, blank=True, default=0
    )

    def __unicode__(self):
        return u"%s %s" % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        if self.sponsor:
            faculty = get_people("faculty")
            try:
                self.sponsor_name = "{} {}".format(
                    faculty[self.sponsor].firstname,
                    faculty[self.sponsor].lastname
                )
                self.sponsor_email = faculty[self.sponsor].email
            except:
                self.sponsor_name = settings.COS_DEFAULT_NAME
                self.sponsor_email = settings.COS_DEFAULT_EMAIL
        super(Presenter, self).save()

    def year(self):
        if self.college_year:
            year = YEAR_CHOICES[int(self.college_year)][1]
        else:
            year = None
        return year

    def presenter_type(self):
        return PRESENTOR_TYPES[self.prez_type][1]


class Presentation(models.Model):
    # meta
    user = models.ForeignKey(
        User, verbose_name="Created by",
        related_name="presentation_created_by"
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="presentation_updated_by", editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    tags = TaggableManager()
    ranking = models.IntegerField(
        null=True, blank=True, default=0
    )
    # core
    title = models.CharField(
        "Presentation title", max_length=255
    )
    reviewer = models.CharField(
        max_length=128,
        null=True, blank=True
    )
    leader = models.ForeignKey(
        Presenter, verbose_name="Presentation leader",
        related_name="presentation_leader", null=True, blank=True
    )
    presenters = models.ManyToManyField(
        Presenter, related_name="presentation_presenters", blank=True
    )
    funding = models.CharField(
        "Funding source (if applicable)", max_length=255,
        help_text="e.g. external funding, SURE, etc.",
        null=True, blank=True
    )
    work_type = models.CharField(
        max_length=32, choices=WORK_TYPES
    )
    permission = models.CharField(
        "Permission to reproduce", max_length=3,
        choices=BINARY_CHOICES,
        help_text = """
            Do you grant Carthage permission to reproduce your presentation?
        """
    )
    shared = models.CharField(
        "Faculty sponsor approval",
        max_length=3, choices=BINARY_CHOICES,
        help_text = """
            Has your faculty sponsor approved your proposal?
            Note: Faculty and staff presenters should choose 'yes'.
        """
    )
    abstract_text = models.TextField(
        "Abstract",
        help_text="Copy and paste your abstract text or start typing."
    )
    need_table = models.CharField(max_length=3, choices=BINARY_CHOICES)
    need_electricity = models.CharField(max_length=3, choices=BINARY_CHOICES)
    poster_file = models.FileField(
        upload_to='files/scholars/posters/{}'.format(YEAR),
        validators=FILE_VALIDATORS,
        help_text="Upload a poster file",
        null=True, blank=True
    )
    status = models.BooleanField(default=False)

    class Meta:
        #ordering        = ('-date_created',)
        ordering        = ('date_created',)
        get_latest_by   = 'date_created'
        permissions     = ( ("manage_presentation", "manage presentation"), )

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
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
                subject = "[Celebration of Scholars] Presentation has been approved"
                send_mail(
                    None,TO_LIST,subject,email,
                    'scholars/presentation/approved_mail.html',self,BCC
                )
        else:
            self.updated_by = self.user
        super(Presentation, self).save()

    def tag_list(self):
        return u", ".join(o.name for o in self.tags.all())

    @models.permalink
    def get_absolute_url(self):
        return ('presentation_detail', [str(self.id)])

    @models.permalink
    def get_update_url(self):
        return ('presentation_update', [str(self.id)])

    def get_presenters(self):
        return self.presenters.order_by('-leader','last_name')

    def get_presenters_print(self):
        return self.presenters.order_by('last_name')

    def mugshot_status(self):
        status = True
        for p in self.presenters.all():
            if not p.mugshot:
                status = False
                break
        return status

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def sponsor(self):
        if self.leader:
            return self.leader.sponsor_email
        else:
            return None

    def sponsor_other(self):
        if self.leader:
            return self.leader.sponsor_other
        else:
            return None

    def poster(self):
        p = False
        if self.poster_file:
            p = mark_safe(u'<a href="https://{}/assets/{}">Download</a>'.format(
                settings.SERVER_URL,self.poster_file)
            )
        return p
    poster.allow_tags = True

    def presentation_type(self):
        return WORK_TYPES[self.work_type][1]

