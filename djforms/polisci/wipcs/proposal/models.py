from django.db import models

from djforms.core.models import GenericContact

from tagging import fields, managers

SUBMITTING =(
    ("Paper for presentation", "Paper for presentation"),
    ("Poster for presentation", "Poster for presentation"),
    ("Roundtable proposal", "Roundtable proposal")
)

class ProposalContact(GenericContact):

    phone = models.CharField(
        verbose_name='Phone number',
        max_length=12,
        help_text="Format: XXX-XXX-XXXX"
    )
    address1 = models.CharField(
        max_length=255,
        verbose_name="Address",
        null=True, blank=True
    )
    address2 = models.CharField(
        verbose_name="",
        max_length=255,
        null=True, blank=True
    )
    city = models.CharField(
        verbose_name="City",
        max_length=128,
        null=True, blank=True
    )
    state = models.CharField(
        verbose_name="State",
        max_length=2,
        null=True, blank=True
    )
    postal_code = models.CharField(
        max_length=10,
        verbose_name="Zip",
        null=True, blank=True
    )
    how_hear = models.CharField(
        "How did you hear about this conference?",
         max_length="128"
    )
    abstract = models.TextField()
    cv = models.FileField(
        'CV', upload_to='files/polisci/wipcs/cv/',
        max_length="256"
    )
    submitting = models.CharField(
        "You are submitting a:",
        max_length="128", choices=SUBMITTING
    )

    class Meta:
        db_table = 'wipcs_proposal'

