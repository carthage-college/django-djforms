from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from djforms.core.models import BINARY_CHOICES

class Profile(models.Model):
    # user data
    user                = models.ForeignKey(User, verbose_name="Created by", related_name="profile_user",editable=False)
    updated_by          = models.ForeignKey(User, verbose_name="Updated by", related_name="profile_updated_by",editable=False)
    # dates
    created_on          = models.DateTimeField("Date Created", auto_now_add=True)
    updated_on          = models.DateTimeField("Date Updated", auto_now=True)
    #core
    department          = models.CharField(max_length=128)
    objective           = models.TextField("What is your Individual Technology Objective (ITO)?")
    partner             = models.CharField("Do you have a partner?", max_length=3, choices=BINARY_CHOICES)
    partner_name        = models.CharField('If you answered "Yes" to Question 2, who is your partner?', max_length=255, null=True, blank=True)
    comments            = models.TextField("Additional Comments", help_text="Please use this space for any extra information you would like to share with us about your ITO. You can also ask questions or express your concerns about the ITOs.", null=True, blank=True)

    class Meta:
        permissions = ( ("ito_can_manage_profile", "Can manage profile"), )
        ordering  = ('-id',)

    def __unicode__(self):
        return u'%s %s' % (self.user.last_name, self.user.first_name)

    def get_absolute_url(self):
        return reverse("profile_detail", args=[self.pk])

    def get_update_url(self):
        return reverse("profile_update", args=[self.pk])

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email
