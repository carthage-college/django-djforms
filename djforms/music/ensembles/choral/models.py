from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from djforms.core.models import YEAR_CHOICES

class TimeSlot(models.Model):
    date_time = models.CharField("Time slot", max_length=128)
    active = models.BooleanField(default=True)
    rank = models.IntegerField(null=True,blank=True)

    class Meta:
        db_table = 'music_ensembles_choral_timeslot'
        ordering = ['id']

    def __unicode__(self):
        return self.date_time

class Candidate(models.Model):
    user = models.ForeignKey(
        User,
        related_name='music_ensemble_choral_candidate',
        on_delete=models.CASCADE,
    )
    # dates
    created_on = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    updated_on = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    #core
    time_slot = models.ForeignKey(
        TimeSlot,
        related_name='music_ensemble_choral_timeslot',
        on_delete=models.CASCADE,
    )
    majors = models.CharField(
        max_length=255
    )
    grad_year = models.CharField(
        "Current Year at Carthage",
        max_length=1, choices=YEAR_CHOICES
    )
    experience = models.TextField(
        "Describe your previous choral experience",
        null=True, blank=True
    )

    class Meta:
        db_table = 'music_ensembles_choral_candidate'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email
