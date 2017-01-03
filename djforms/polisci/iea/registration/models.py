from django.db import models
from django.utils.safestring import mark_safe

from djforms.processors.models import Contact

from djtools.fields import BINARY_CHOICES

from tagging import fields, managers

SERVE_AS_CHOICES = (
    ('Discussant', 'Discussant'),
    ('Session Chair/Moderator', 'Session Chair/Moderator'),
)
PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Check', 'Check'),
)
REGGIES = (
    ('Early Registration|300','$300 Early Registration (due by May 31, 2017)'),
    ('Graduate Student|125','$125 Graduate Student'),
    (
        'Undergraduate Student|100',
        mark_safe(
            '''
            $100 Undergraduate Student (Verification Required)
            <strong>&dagger;</strong>
            '''
        )
    ),
    (
        'Spouses/companions|75',
        mark_safe(
            '$75 Spouses/companions <strong>&dagger;</strong>'
        )
    ),
    (
        'Panel/session organizers|150',
        mark_safe(
            '$150 Panel/session organizers <strong>&dagger;&dagger;</strong>'
        )
    ),
    (
        'Local Participants|100',
        mark_safe(
            '$100 Local Participants <strong>&dagger;&dagger;&dagger;</strong>'
        )
    ),
)


class RegistrationContact(Contact):

    institution = models.CharField(
         max_length=128
    )
    serve_as = models.CharField(
        max_length=128,
        choices=SERVE_AS_CHOICES,
        null=True, blank=True,
        help_text='''
            If so, please provide your Discipline and Specialty below.
        '''
    )
    discipline = models.CharField(
        max_length=128,
        null=True, blank=True
    )
    specialty = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    registration_fee = models.CharField(
        max_length=128,
        choices=REGGIES
    )
    # registrants
    kao_member = models.CharField(
        max_length=4,
        choices=BINARY_CHOICES,
        help_text = 'KAO Members receive a $50 discount on the Registration Fee.'
    )
    # payment
    payment_method = models.CharField(
        max_length=128,
        choices=PAYMENT_CHOICES
    )

    class Meta:
        db_table = 'iea_registration_contact'

