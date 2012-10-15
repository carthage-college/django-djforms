from django.db import models
from django.contrib.auth.models import User

from djforms.core.models import GenericChoice, SHIRT_SIZES, YEAR_CHOICES
from djforms.core.models import Department

from tagging import fields, managers

WORK_TYPES = (
    ('','----select----'),
    ('SURE','SURE'),
    ('Thesis','Thesis'),
    ('Course work','Course work'),
    ('Other','Other')
)

PRESENTER_TYPES = (
    ('','----select----'),
    ('Student','Student'),
    ('Faculty','Faculty'),
    ('Staff','Staff'),
)

class Presenter(models.Model):
    date_created        = models.DateTimeField("Date Created", auto_now_add=True)
    date_updated        = models.DateTimeField("Date Updated", auto_now=True)
    first_name          = models.CharField(max_length=128, null=True, blank=True)
    last_name           = models.CharField(max_length=128, null=True, blank=True)
    leader              = models.BooleanField("Presentation leader", default=False)
    prez_type           = models.CharField("Presenter type", max_length="16", choices=PRESENTER_TYPES, null=True, blank=True)
    college_year        = models.CharField("Current year at Carthage", max_length="1", choices=YEAR_CHOICES, null=True, blank=True)
    major               = models.CharField(max_length=128, null=True, blank=True)
    hometown            = models.CharField(max_length=128, null=True, blank=True)
    sponsor             = models.CharField(max_length=128, null=True, blank=True)
    department          = models.ForeignKey(Department, null=True, blank=True)
    shirt               = models.CharField(max_length=2, choices=SHIRT_SIZES, null=True, blank=True)
    mugshot             = models.ImageField(max_length=255, upload_to="files/scholars/mugshots", help_text="75 dpi and .jpg only", null=True, blank=True)
    ranking             = models.IntegerField(null=True, blank=True, default=0)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def year(self):
        return YEAR_CHOICES[int(self.college_year)][1]

    def presenter_type(self):
        return PRESENTOR_TYPES[self.prez_type][1]

    def shirt_size(self):
        return SHIRT_SIZES[self.shirt][1]

class Presentation(models.Model):
    # meta
    user                = models.ForeignKey(User, verbose_name="Created by", related_name="presentation_created_by",editable=False)
    updated_by          = models.ForeignKey(User, verbose_name="Updated by", related_name="presentation_updated_by",editable=False)
    date_created        = models.DateTimeField("Date Created", auto_now_add=True)
    date_updated        = models.DateTimeField("Date Updated", auto_now=True)
    tags                = fields.TagField(blank=True, null=True, default='', help_text="Seperate multiple tags with a space, or use comma if a tag contains more than one word.")
    ranking             = models.IntegerField(null=True, blank=True, default=0)
    # tag object manager
    tag_objects         = managers.ModelTaggedItemManager()
    # Default object manager
    objects             = models.Manager()
    # core
    title               = models.CharField("Presentation title", max_length=256)
    leader              = models.ForeignKey(Presenter, verbose_name="Presentation leader", related_name="presentation_leader", null=True, blank=True)
    presenters          = models.ManyToManyField(Presenter, related_name="presentation_presenters", null=True, blank=True)
    funding             = models.TextField(null=True, blank=True)
    requirements        = models.TextField(null=True, blank=True)
    work_type           = models.CharField(max_length=32, choices=WORK_TYPES)
    work_type_other     = models.CharField(max_length=256, null=True, blank=True)
    permission          = models.BooleanField(help_text="Do you grant Carthage permission to reproduce your presentation?", default=True)
    shared              = models.BooleanField(help_text="Has your faculty sponsor approved your proposal?", default=True)
    abstract_text       = models.TextField(null=True, blank=True, help_text='')
    abstract_file       = models.FileField(upload_to='files/scholars/abstracts', max_length="256", help_text='Upload an abstract in PDF format', null=True, blank=True)
    poster_file         = models.FileField(upload_to='files/scholars/posters', max_length="256", help_text='Upload a poster file', null=True, blank=True)
    status              = models.BooleanField(default=False)

    class Meta:
        ordering        = ('-date_created',)
        get_latest_by   = 'date_created'
        permissions     = ( ("manage_presentation", "manage presentation"), )

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('presentation_detail', [str(self.id)])

    @models.permalink
    def get_update_url(self):
        return ('presentation_update', [str(self.id)])

    def get_presenters(self):
        return self.presenters.order_by('-leader','last_name')

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

    def phone(self):
        return self.user.get_profile().phone

    def presentation_type(self):
        return WORK_TYPES[self.work_type][1]
