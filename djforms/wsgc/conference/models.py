# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe
from djforms.processors.models import Contact
from djtools.fields import BINARY_CHOICES


PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Check', 'Check'),
)
REGGIES = (
    (
        'Early Registration|275',
        mark_safe(
            """
            $275 Early Registration (due by May 1, 2019)
            <strong>&dagger;&dagger;</strong>
            """
        )
    ),
    ('Graduate Student|125','$125 Graduate Student'),
    (
        'Undergraduate Student|75',
        mark_safe(
            """
            $75 Undergraduate Student (Verification Required)
            <strong>&dagger;</strong>
            """
        )
    ),
    (
        'Spouses/companions|75',
        mark_safe(
            "$75 Spouses/companions <strong>&dagger;</strong>"
        )
    ),
    (
        'Local Participants|75',
        mark_safe(
            """
            $75 Local Puerto Rico Participants
            <strong>&dagger;&dagger;&dagger;</strong>
            """
        )
    )
)


class RegistrationContact(Contact):
    """Conference registration data model."""

    institution = models.CharField(
         max_length=128
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
    wsgc_member = models.CharField(
        "Do you have WSGC membership?",
        max_length=4,
        choices=BINARY_CHOICES,
        help_text = """
            WSGC Members receive a $50 discount on the Registration Fee.
        """
    )
    # payment
    payment_method = models.CharField(
        max_length=128,
        choices=PAYMENT_CHOICES
    )

    class Meta:
        db_table = 'wsgc_registration_contact'
