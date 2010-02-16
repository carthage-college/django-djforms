from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.localflavor.us.models import USStateField
from djforms.core.models import Photo, GenericContact

class Questionnaire(GenericContact):
    address         = models.CharField(max_length=255, verbose_name = 'Address')
    city            = models.CharField(max_length=128, verbose_name = 'City')
    state           = USStateField()
    zip             = models.CharField(max_length=10, verbose_name = 'Zip code')
    phone           = models.CharField(max_length=12, verbose_name='Phone Number', help_text="Format: XXX-XXX-XXXX")
    occupation1     = models.CharField(max_length=100, verbose_name = 'Occupation', help_text = 'What someone pays you to do.', null=True, blank=True)
    occupation2     = models.CharField(max_length=100, verbose_name = 'Occupation', help_text = 'What no one pays you to do but you do anyway.', null=True, blank=True)
    website         = models.CharField(max_length=100, verbose_name = 'What is your favorite website?', null=True, blank=True)
    website_why     = models.TextField('Why?', null=True, blank=True)
    challenge       = models.TextField('What has challenged you most about the "Real" world?', null=True, blank=True)
    professor       = models.CharField(max_length=100, verbose_name = 'Who was your favorite Carthage professor?', null=True, blank=True)
    professor_why   = models.TextField('Why?', null=True, blank=True)
    relive          = models.TextField('If you had the chance to relive a single Carthage moment or event, which one would you choose?', null=True, blank=True)
    message         = models.TextField('Personal message', help_text="You may want to include family, hobbies, travel experiences and fond rememberances.", null=True, blank=True)
    photos          = models.ManyToManyField(Photo, verbose_name="Photos", related_name="alumni_memory_questionaire_photos", null=True, blank=True)

    class Meta:
        db_table = 'alumni_memory_questionnaire'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("memory_questionnaire_detail", args=[self.pk])
