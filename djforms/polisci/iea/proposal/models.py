from django.db import models

from djforms.processors.models import Contact

from djtools.fields.helpers import upload_to_path
from djtools.fields.validators import MimetypeValidator

from django_countries.fields import CountryField

# comment out for migrations
FILE_VALIDATORS = [MimetypeValidator('application/pdf')]
#FILE_VALIDATORS = []

PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Check', 'Check'),
)
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
    abstract = models.FileField(
        upload_to=upload_to_path,
        max_length=768,
        validators=FILE_VALIDATORS,
        help_text="PDF format"
    )
    submitting = models.CharField(
        "You are submitting a:",
        max_length=128, choices=SUBMITTING
    )
    # payment
    payment_method = models.CharField(
        max_length=128,
        choices=PAYMENT_CHOICES
    )

    class Meta:
        db_table = 'iea_proposal_contact'

    def get_slug(self):
        return 'files/polisci/iea/proposal/'

