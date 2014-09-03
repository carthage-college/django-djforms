from django.db import models

from djforms.processors.models import Contact

from tagging import fields, managers

PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Check', 'Check'),
)

class RegistrationContact(Contact):

    how_hear = models.CharField(
        "How did you hear about this conference?",
         max_length="128"
    )
    payment_method = models.CharField(
        max_length="128",
        choices=PAYMENT_CHOICES
    )

    class Meta:
        db_table = 'wipcs_registration'

