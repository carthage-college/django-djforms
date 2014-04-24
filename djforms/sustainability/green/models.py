from django.db import models
from django.contrib.auth.models import User
from djforms.core.models import BINARY_CHOICES

class Pledge(models.Model):
    # user data
    user                = models.ForeignKey(User, verbose_name="Created by", related_name="pledge_user",editable=False)

    class Meta:
        ordering  = ('-id',)

    def __unicode__(self):
        return u'%s %s' % (self.user.last_name, self.user.first_name)

    def get_absolute_url(self):
        return "https://www.carthage.edu/directory/%s/modal/" % self.user.email.split('@')[0]

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

