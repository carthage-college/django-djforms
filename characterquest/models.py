from django.db import models
from djforms.core.models import UserProfile

BINARY_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)

class ApplicationProfile(models.Model):
    profile                     = models.ForeignKey(UserProfile)

    organizations               = models.TextField("Organizations and Activities",
                                        help_text="Please list below\
                                  all campus activities and organization with\
                                  which you are involved.  Also list any\
                                  positions you currently hold, and the number\
                                  of years you have been involved with each\
                                  organization.")
    skills_experience           = models.TextField("Why you?",
                                        help_text="Why do you want to be part\
                                  of the Character Quest Leadership\
                                  Certification process, and how will you\
                                  utilize it during your time at Carthage?")
    why_orientation_leader      = models.TextField("Leadership Acumen",
                                        help_text="What do you believe are the\
                                  qualities of an effective leader?")
    describe_experience         = models.TextField("Leadership Experience",
                                        help_text="Describe an experience\
                                  that, for you, demonstrates what leadership\
                                  at Carthage is all about.")
    references                  = models.TextField("References",
                                        help_text="Please list two references\
                                  along with their phone numbers. References\
                                  should be Carthage faculty, staff, coaching\
                                  staff or advisors.")

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
