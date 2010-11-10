from django.db import models
from djforms.core.models import UserProfile

class ApplicationProfile(models.Model):
    profile         = models.ForeignKey(UserProfile)
    mobile          = models.CharField(max_length=12, verbose_name='Mobile Phone', help_text="Format: XXX-XXX-XXXX", null=True, blank=True)
    high_school     =
    hs_city         =
    hs_state        =
    hs_grad_year    =
    entry_as        =
    entry_year      =
    entry_term      = models.CharField()
    academic        = models.TextField("Academic Interests")
    extracurricular = models.TextField("Extracurricular Interests")
    comments        = models.TextField(null=True, blank=True)

    def first_name(self):
        return self.profile.user.first_name
    def last_name(self):
        return self.profile.user.last_name
    def email(self):
        return self.profile.user.email
    def phone(self):
        return self.profile.phone
    def address(self):
        return self.profile.address
    def city(self):
        return self.profile.city
    def state(self):
        return self.profile.state
    def zip(self):
        return self.profile.zip
    def gender(self):
        return self.profile.gender
