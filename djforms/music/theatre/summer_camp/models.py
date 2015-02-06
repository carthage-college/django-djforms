from django.db import models

from djtools.fields import GENDER_CHOICES
from djforms.processors.models import Contact

VOICE_TYPE = (
    ('Soprano/Legit','Soprano/Legit'),
    ('Belter','Belter'),
    ('Tenor','Tenor'),
    ('Bass/Baritone','Bass/Baritone'),
)
HOW_HEAR = (
    ('Web','Web'),
    ('Referred by a teacher','Referred by a teacher'),
    ('Print flier','Print flier'),
)
PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Bank Transfer', 'Bank Transfer'),
)

class SummerCampAttender(Contact):

    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=32
    )
    voice_type = models.CharField(
        choices=VOICE_TYPE, max_length=32
    )
    dob = models.DateField(
        "Date of birth", help_text="Format: mm/dd/yyyy"
    )
    school = models.CharField(
        "School or university currently attending",
        max_length=255
    )
    how_hear = models.CharField(
        "How did you hear about our Summer Camp in Music Theatre?",
        choices=HOW_HEAR, max_length=32
    )
    payment_method = models.CharField(
        choices=PAYMENT_CHOICES, max_length=24
    )

    class Meta:
        db_table = 'music_theatre_summer_camp'

