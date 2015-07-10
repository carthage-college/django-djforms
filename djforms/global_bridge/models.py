from django.db import models

from djforms.processors.models import Contact

from djtools.fields import GENDER_CHOICES


PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Bank Transfer', 'Bank Transfer'),
)

class Registration(Contact):

    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=32
    )
    dob = models.DateField(
        "Date of birth", help_text="Format: mm/dd/yyyy"
    )
    school = models.CharField(
        "School or university currently attending",
        max_length=255
    )
    payment_method = models.CharField(
        choices=PAYMENT_CHOICES, max_length=24
    )

    class Meta:
        db_table = 'global_bridge_registration'

