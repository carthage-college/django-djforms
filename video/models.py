from django.db import models
from django.contrib.auth.models import User

from djforms.core.models import YEAR_CHOICES
from tagging import fields, managers

class Contest(models.Model):
    # Default object manager
    objects = models.Manager()
    # core
    user                = models.ForeignKey(User, verbose_name="Created by", related_name="contest_user",editable=False)
    updated_by          = models.ForeignKey(User, verbose_name="Updated by", related_name="contest_updated_by",editable=False)
    college_year        = models.CharField("Current Year at Carthage", max_length="1", choices=YEAR_CHOICES)
    url                 = models.URLField("Video URL", verify_exists=False, max_length=255)
    title               = models.CharField(max_length=128)
    description         = models.TextField("Description")
    # dates
    created_on          = models.DateTimeField("Date Created", auto_now_add=True)
    updated_on          = models.DateTimeField("Date Updated", auto_now=True)
    # meta
    tags = fields.TagField(blank=True, null=True)
    # tag object manager
    tag_objects = managers.ModelTaggedItemManager()

    class Meta:
        ordering  = ('-created_on',)
        get_latest_by = 'created_on'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def phone(self):
        return self.user.get_profile().phone

    def year(self):
        return YEAR_CHOICES[self.college_year][1]

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return self.url

    #def save(self, *args, **kwargs):
    #    if self.id:
    #    super(Contest, self).save(*args, **kwargs)

