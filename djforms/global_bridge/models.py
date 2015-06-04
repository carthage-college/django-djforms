from django.db import models

from djforms.core.models import GenericContact

from djtools.fields import GENDER_CHOICES

HOW_HEAR = (
    ('Web','Web'),
    ('Referred by a teacher','Referred by a teacher'),
    ('Print flier','Print flier'),
)

class Registration(GenericContact):

    phone = models.CharField(
        verbose_name='Phone number',
        max_length=18,
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
        max_length=128,
        null=True, blank=True
    )
    postal_code = models.CharField(
        max_length=10,
        verbose_name="Zip",
        null=True, blank=True
    )
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
    how_hear = models.CharField(
        "How did you hear about our Summer Camp in Music Theatre?",
        choices=HOW_HEAR, max_length=32
    )

    class Meta:
        db_table = 'global_bridge_registration'

