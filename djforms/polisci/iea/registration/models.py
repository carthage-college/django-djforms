from django.db import models
from django.utils.safestring import mark_safe

from djforms.processors.models import Contact

from djtools.fields import BINARY_CHOICES


SERVE_AS_CHOICES = (
    ('Discussant', 'Discussant'),
    ('Session Chair/Moderator', 'Session Chair/Moderator'),
)
PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Check', 'Check'),
)
REGGIES = (
    (
        'Early Registration|275',
        mark_safe(
            """
            $275 USD Early Registration (due by May 1, 2019)
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

    institution = models.CharField(
         max_length=128
    )
    serve_as = models.CharField(
        max_length=128,
        choices=SERVE_AS_CHOICES,
        null=True, blank=True,
        help_text="""
            If so, please provide your Discipline and Specialty below.
        """
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
        "Do you have KAO membership?",
        max_length=4,
        choices=BINARY_CHOICES,
        help_text = """
            KAO Members receive a $50 discount on the Registration Fee.
        """
    )
    # abstract registrants
    abstract = models.CharField(
        "Did you submit an abstract and pay the $50 fee?",
        max_length=4,
        choices=BINARY_CHOICES,
        help_text = """
            Registrants who submitted an abstract and paid the fee receive a
            $50 discount on the Registration Fee.
        """
    )
    # payment
    payment_method = models.CharField(
        max_length=128,
        choices=PAYMENT_CHOICES
    )

    class Meta:
        db_table = 'iea_registration_contact'

