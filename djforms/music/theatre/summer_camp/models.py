from django.db import models

from djtools.fields import GENDER_CHOICES
from djforms.processors.models import Contact

VOICE_TYPE = (
    ('','---------'),
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

    """
citizenship:

Province/territory
country
postal code [ in China are a numeric six-digit system for the whole country.]
phone number with country code (+86 xxx XXXX YYYY)
    [no need for country code if all are from china, no?]


Payment:
     total cost is $2,800
     The $2,800 camp fee is due by June 10, 2015. Refunds may be requested prior to the June 10 deadline. After June 10, 2015, a partial refund may be requested. After July 1, 2015, no refunds will be given.

      options for them to pay $2,800 include transfer, credit card...
    """
