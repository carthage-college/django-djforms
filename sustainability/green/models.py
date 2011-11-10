from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from djforms.core.models import BINARY_CHOICES

class Pledge(models.Model):
    # user data
    user                = models.ForeignKey(User, verbose_name="Created by", related_name="pledge_user",editable=False)
    #core
    comments            = models.TextField("Comments (optional)", help_text="Please use this space for your thoughts on sustainability that you would like to share with the Carthage community.", null=True, blank=True)

    class Meta:
        ordering  = ('-id',)

    def __unicode__(self):
        return u'%s %s' % (self.user.last_name, self.user.first_name)

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

