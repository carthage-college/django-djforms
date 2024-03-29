# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from djforms.core.models import YEAR_CHOICES


class TimeSlot(models.Model):
    """Data model for the time slots of the choral tryout form."""

    date_time = models.CharField("Time slot", max_length=128)
    active = models.BooleanField(default=True)
    rank = models.IntegerField(null=True, blank=True)

    class Meta:
        """Subclass for defining setings about the parent class."""

        db_table = 'music_ensembles_choral_timeslot'
        ordering = ['id']

    def __str__(self):
        """Default display value."""
        return self.date_time


class Candidate(models.Model):
    """Data model for the candidate of the choral tryout form."""

    user = models.ForeignKey(
        User,
        related_name='music_ensemble_choral_candidate',
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField("Date Created", auto_now_add=True)
    updated_on = models.DateTimeField("Date Updated", auto_now=True)
    time_slot = models.ForeignKey(
        TimeSlot,
        related_name='music_ensemble_choral_timeslot',
        on_delete=models.CASCADE,
    )
    majors = models.CharField(max_length=255)
    grad_year = models.CharField(
        "Current Year at Carthage",
        max_length=1,
        choices=YEAR_CHOICES,
    )
    experience = models.TextField(
        "Describe your previous choral experience",
        null=True,
        blank=True,
    )

    class Meta:
        """Subclass for defining setings about the parent class."""

        db_table = 'music_ensembles_choral_candidate'
        ordering = ['-created_on']

    def first_name(self):
        """Display the user's given name."""
        return self.user.first_name

    def last_name(self):
        """Display the user's sur name."""
        return self.user.last_name

    def email(self):
        """Display the user's email."""
        return self.user.email
