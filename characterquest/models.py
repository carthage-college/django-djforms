from django.db import models
from djforms.core.models import UserProfile

BINARY_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

class ApplicationProfile(models.Model):
    profile                     = models.ForeignKey(UserProfile)

    organizations               = models.TextField("Oganizations and Activities",
                                                   help_text="Please list below\
                                  all campus activities and organization with\
                                  which you are involved.  Also list any\
                                  positions you currently hold, and the number\
                                  of years you have been involved with each\
                                  organization.")
    skills_experience           = models.TextField("What skills/experience\
                                  should a successful orientation leader have?")
    why_orientation_leader      = models.TextField("Why do you want to be an\
                                  orientation leader?")
    describe_experience         = models.TextField("Describe an experience\
                                  that, for you, demonstrates what Carthage is\
                                  all about.")

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
    def sex(self):
        return self.profile.sex
