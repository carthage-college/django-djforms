from django.db import models

from djforms.processors.models import Contact

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


class ProposalContact(Contact):

    presenter_type = models.CharField(
        "I am a",
        max_length=128, choices=PRESENTER_TYPE
    )
    affiliation = models.CharField(
        "Academic or university affiliation",
         max_length=255
    )
    how_hear = models.CharField(
        "How did you hear about this conference?",
         max_length=128
    )
    abstract = models.TextField()
    submitting = models.CharField(
        "You are submitting a:",
        max_length=128, choices=SUBMITTING
    )

    class Meta:
        db_table = 'iea_proposal_contact'
