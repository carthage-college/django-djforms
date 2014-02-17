from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from djforms.core.models import GenericContact

"""
Model: Alumna Contact

we can obtain all classnotes via the backward relationships
https://docs.djangoproject.com/en/dev/topics/db/queries/#following-relationships-backward

c     = Contact.objects.get(id=1)
notes = c.note_set.all()
rels  = c.relation_set.all()
"""

class Relation(models.Model):
    class Meta:
        db_table = 'alumni_contact_relation'


class Address(models.Model):
    class Meta:
        db_table = 'alumni_contact_address'


class Organization(models.Model):
    class Meta:
        db_table = 'alumni_contact_organization'


class SocialMedia(models.Model):
    class Meta:
        db_table = 'alumni_contact_socialmedia'


class Privacy(models.Model):
    class Meta:
        db_table = 'alumni_contact_socialmedia'


class Contact(GenericContact):
    user                = models.OneToOneField(User)
    carthage_id         = models.CharField(max_length=8)
    second_name         = models.CharField("Middle name", max_length=128, null=True, blank=True)
    previous_name       = models.CharField("Previous name", max_length=128, help_text="e.g. Maiden name", null=True, blank=True)
    salutation          = models.CharField(max_length=16, null=True, blank=True,help_text="e.g. Ms., Mr. Dr.")
    suffix              = models.CharField(max_length=16, null=True, blank=True,help_text="e.g. PhD., Esquire, Jr., Sr., III")
    is_deceased         = models.BooleanField(default=False)
    classyear           = models.CharField("Class", max_length=4)
    degree              = models.CharField(max_length=255)
    major1              = models.CharField("Major 1", max_length=255)
    major2              = models.CharField("Major 2", max_length=255, blank=True, null=True)
    minor1              = models.CharField("Minor 1", max_length=255, blank=True, null=True)
    minor2              = models.CharField("Minor 2", max_length=255, blank=True, null=True)
    honorary_degree     = models.CharField("Honorary Degree Received", max_length=255, blank=True, null=True)
    distinguished       = models.CharField("Distinguished Alumni Award Received", max_length=255, blank=True, null=True)
    masters_grad_year   = models.CharField("Masters Graduation Year", max_length=4, blank=True, null=True)
    phd_grad_year       = models.CharField("Doctorate Graduation Year", blank=True, null=True)
    job_title           = models.CharField(max_length=255, blank=True, null=True)
    # classnote
    spouse_name         = models.CharField("Spouse's name", max_length=128, blank=True, null=True)
    spouse_previous_name= models.CharField("Spouse's previous name", max_length=32, help_text="e.g. maiden name", blank=True, null=True)
    spouse_year         = models.CharField("Spouse's class", max_length=4, blank=True, null=True)
    spouse_carthage     = models.OneToOneField(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="alumni_carthage_spouse")
    # social
    contacts            = models.ManyToManyField(User, blank=True, null=True, related_name="alumni_contacts")
    # meta
    privacy             = models.OneToOneField(Privacy, related_name="alumni_privacy")
    status              = models.BooleanField(default=False, help_text="Is the data ready for public viewing?")

    class Meta:
        db_table = 'alumni_contact'
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __unicode__(self):
        return "%s, %s (%s)" % (self.last_name, self.first_name, self.classyear)

    def get_edit_url(self):
        #return reverse(change_stage, args=["directory", "contact", self.id] )
        return "http://%s/forms/admin/classnotes/contact/%s/" % (settings.SERVER_URL, self.id)

