from django.db import models

from djforms.core.models import GenericContact

from django_countries.fields import CountryField

SUBMITTING = (
    ("Creative Presentation", "Creative Presentation"),
    ("Paper for presentation", "Paper for presentation"),
    ("Poster for presentation", "Poster for presentation"),
    ("Roundtable proposal", "Roundtable proposal")
)

PRESENTER_TYPE = (
    ("Professor", "Professor"),
    ("Graduate Student", "Graduate Student"),
    ("Undergraduate Student", "Undergraduate Student"),
    ("Activist", "Activist"),
    ("Other", "Other")
)


class ProposalContact(GenericContact):

    phone = models.CharField(
        verbose_name='Phone number',
        max_length=16
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
        null=True, blank=True
    )
    presenter_type = models.CharField(
        "I am a",
        max_length="128", choices=PRESENTER_TYPE
    )
    country = CountryField(
        blank_label='(select country)',
        null=True, blank=True
    )
    affiliation = models.CharField(
        "Academic or university affiliation",
         max_length="255"
    )
    how_hear = models.CharField(
        "How did you hear about this conference?",
         max_length="128"
    )
    abstract = models.TextField()
    submitting = models.CharField(
        "You are submitting a:",
        max_length="128", choices=SUBMITTING
    )

    class Meta:
        db_table = 'iea_proposal_contact'

