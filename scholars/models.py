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

PRESENTOR_TYPES = (
    ('','----select----'),
    ('Student','Student'),
    ('Faculty','Faculty'),
    ('Staff','Staff'),
    ('Other','Other')
)

class Presenter(models.Model):
    first_name          = models.CharField(max_length=128)
    last_name           = models.CharField(max_length=128)
    leader              = models.BooleanField("Presentation leader")
    prez_type           = models.CharField("Presenter type", max_length="16", choices=PRESENTOR_TYPES)
    college_year        = models.CharField("Current year at Carthage", max_length="1", choices=YEAR_CHOICES)
    major               = models.CharField(max_length=128)
    hometown            = models.CharField(max_length=128)
    sponsor             = models.CharField(max_length=128, null=True, blank=True)
    department          = models.ForeignKey(Department, null=True, blank=True)
    shirt               = models.CharField(max_length=2, choices=SHIRT_SIZES)
    mugshot             = models.ImageField(max_length=255, upload_to="files/scholars/mugshots", help_text="75 dpi and .jpg only")
    ranking             = models.IntegerField(null=True, blank=True, default=0)

    def year(self):
        return YEAR_CHOICES[self.college_year][1]

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
    title               = models.CharField("Presentation title", max_length=128)
    leader              = models.ForeignKey(Presenter, verbose_name="Presentation leader", related_name="presentation_leader",editable=False)
    presenters          = models.ManyToManyField(Presenter, related_name="presentation_presenters", null=True, blank=True)
    funding             = models.TextField(null=True, blank=True)
    requirements        = models.TextField(null=True, blank=True)
    work_type           = models.CharField(max_length=2, choices=WORK_TYPES)
    permission          = models.BooleanField(help_text="Do you grant Carthage permission to reproduce your presentation?")
    abstract_text       = models.TextField(null=True, blank=True, help_text='')
    abstract_file       = models.FileField(upload_to='files/scholars/abstracts', max_length="256", help_text='Upload an abstract in PDF format', null=True, blank=True)

    class Meta:
        ordering  = ('-date_created',)
        get_latest_by = 'date_created'

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('presentation_detail', [str(self.id)])

    @models.permalink
    def get_update_url(self):
        return ('presentation_update', [str(self.id)])

    def get_presenters(self):
        presenters = []
        for p in self.presenters.all:
            if not p.leader:
                presenters.append(p)

        return presenters

    def get_students(self):
        students = []
        for s in self.presenters.all:
            if not s.leader and s.prez_type=="Student":
                students.append(s)
        return students

    def get_faculty(self):
        faculty = []
        for f in self.presenters.all:
            if f.prez_type=="Faculty":
                faculty.append(f)
        return faculty

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


