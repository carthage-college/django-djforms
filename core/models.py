from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField

from tagging.fields import TagField
from tagging.models import Tag
from imagekit.models import ImageModel
from userprofile.models import BaseProfile

import datetime

SEX_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)
YEAR_CHOICES = (
    ('','---------'),
    ('1','Freshman'),
    ('2','Sophmore'),
    ('3','Junior'),
    ('4','Senior')
)
#For making choices for choice fields for forms
class GenericChoice(models.Model):
    name = models.CharField(unique=True, max_length=255)
    value = models.CharField(max_length=255)
    ranking = models.IntegerField(null=True, blank=True, default=0, max_length=3, verbose_name="Ranking", help_text='A number from 0 to 999 to determine this object\'s position in a list.')
    active = models.BooleanField(help_text='Do you want the field to be visable on your form?', verbose_name='Is active?', default=True)
    tags = TagField()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['ranking']

#For making contacts for forms
class GenericContact(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=126)
    email = models.EmailField()

    class Meta:
        abstract = True
        ordering = ['last_name']

    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)

#For making a generic Contact form
class GenericContactForm(models.Model):
    name = models.CharField(max_length=128)
    slug = models.CharField(max_length=255, verbose_name="Slug", unique=True)
    description = models.TextField('Form Description')
    form_class = models.CharField(max_length=255, verbose_name="Form Class name", unique=True)
    template = models.CharField(max_length=255)
    recipients = models.ManyToManyField(User, related_name='contact_form_recipients')
    is_public = models.BooleanField(default=True, help_text="Is the form available for public viewing?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

class UserProfile(BaseProfile):
    """
    User profile model
    """
    phone   = models.CharField(max_length=12, verbose_name='Phone Number', help_text="Format: XXX-XXX-XXXX")
    address = models.CharField(max_length=255, verbose_name = 'Address', null=True, blank=True)
    city    = models.CharField(max_length=128, verbose_name = 'City', null=True, blank=True)
    state   = USStateField()
    zip     = models.CharField(max_length=10, verbose_name = 'Zip code', null=True, blank=True)
    dob     = models.DateField("Birthday", null=True, blank=True)
    sex     = models.CharField(max_length="16", choices=SEX_CHOICES, null=True, blank=True)
    campus_address  = models.CharField("Campus Address",max_length="64")
    campus_box = models.CharField("Campus Box #",max_length="4")
    college_access_code = models.CharField("Carthage Access Code",max_length="7")
    college_id = models.CharField("Carthage ID", max_length="7")
    college_year = models.CharField("Current Year at Carthage",max_length="1",choices=YEAR_CHOICES)
    permission = models.ManyToManyField(GenericChoice, verbose_name='Permissions', null=True, blank=True,)

    def __unicode__(self):
        return "%s %s's profile with username: %s" % (self.user.first_name, self.user.last_name, self.user.username)

class Photo(ImageModel):
    title = models.CharField(max_length=256)
    original_image = models.ImageField(upload_to='photos/alumemory', max_length="256")
    caption = models.TextField('Caption')
    num_views = models.PositiveIntegerField(editable=False, default=0)

    class IKOptions:
        # This inner class is where we define the ImageKit options for the model
        spec_module = 'djforms.core.photo_specs'
        cache_dir = 'photos/cache'
        image_field = 'original_image'
        save_count_as = 'num_views'

    def _save_FIELD_file(self, field, filename, raw_contents, save=True):
        filename = "%s_%s" % (self.id, filename)
        super(Patch, self)._save_FIELD_file(field, filename, raw_contents, save)

    def __unicode__(self):
        return self.title

    #def get_absolute_url(self):
    #    return reverse("photo_details", args=[self.pk])

STATE_CHOICES = (
    ('','------------'),
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AS', 'American Samoa'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('GU', 'Guam'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('MP', 'Northern Mariana Islands'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('PR', 'Puerto Rico'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VI', 'Virgin Islands'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)