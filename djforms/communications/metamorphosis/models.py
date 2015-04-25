from django.db import models
from django.core.urlresolvers import reverse

from djforms.core.models import Photo


class Questionnaire(models.Model):
    your_name = models.CharField(
        max_length=128
    )
    student_name = models.CharField(
        "Your student's name",
        max_length=128
    )
    email =  models.EmailField(
        "Your email address",
        max_length=128
    )
    hometown = models.CharField(
        max_length=128
    )
    how_changed = models.TextField(
        "How has your student changed since his or her freshman year?"
    )
    comments = models.TextField(
        "Additional comments?"
    )
    photos = models.ManyToManyField(
        Photo, verbose_name = "Photos",
        related_name = "metamorphosis_questionaire_photos",
        null=True, blank=True
    )
    status = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("metamorphosis_detail", args=[self.pk])

    def get_slug(self):
        return "communications/metamorphosis/"
