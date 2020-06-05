from django.db import models
from django.conf import settings

from djtools.fields import GENDER_CHOICES, BINARY_CHOICES, PAYMENT_CHOICES
from djtools.fields import STATE_CHOICES
from djforms.processors.models import Contact

YEAR_CHOICES = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10 or more'),
)

SHIRT_SIZES = (
    ('', '---------'),
    ('Adult S', 'Adult S'),
    ('Adult M', 'Adult M'),
    ('Adult L', 'Adult L'),
    ('Adult XL', 'Adult XL'),
    ('Youth S', 'Youth S'),
    ('Youth M', 'Youth M'),
    ('Youth L', 'Youth L'),
    ('Youth XL', 'Youth XL'),
)

SESSIONS = (
    (
        'Girls resident|495',
        'Girls Resident $495.00 (Goalkeepers check here too: no additional fee)',
    ),
    (
        'Girls commuter|395', 'Girls Commuter $395.00',
    ),
    (
        'Boys & Girls Jr. Kickers Session I|100',
        'Boys & Girls Jr. Kickers Session I $100.00',
    ),
    (
        'Boys resident|495',
        'Boys Resident $495.00 (Goalkeepers check here too: no additional fee)',
    ),
    (
        'Boys commuter|395', 'Boys Commuter $395.00',
    ),
    (
        'Boys & Girls day camp|195', 'Boys & Girls Day camp $195.00',
    ),
    (
        'Boys & Girls Jr. Kickers Session II|100',
        'Boys & Girls. Jr. Kickers Session II $100.00',
    ),
    (
        'Soccer mom camp|245', 'Soccer Mom Camp $245',
    ),
)

AMOUNT_CHOICES = (
    ('Deposit', 'Deposit'),
    ('Full amount', 'Full amount'),
)

REQ = {'class': 'required'}


class SoccerCampAttender(Contact):
    """A model to save registration data for the summer soccer camp."""

    # personal info
    gender = models.CharField(
        choices=GENDER_CHOICES, max_length=32,
    )
    dob = models.DateField(
        "Date of birth", help_text="Format: mm/dd/yyyy"
    )
    age = models.CharField(max_length=2)
    years_attend = models.CharField(
        "Number of years attended",
        choices=YEAR_CHOICES,
        max_length=2,
        help_text="Include this year",
    )
    goalkeeper = models.CharField(
        "Goalkeeper?", choices=BINARY_CHOICES, max_length=4,
    )
    shirt_size = models.CharField(
        "T-shirt size", choices=SHIRT_SIZES, max_length=24,
    )
    # contact info
    parent_guard = models.CharField(
        "Parent or guardian name", max_length=128,
    )
    # housing
    roommate = models.CharField(
        "Roommate request",
        max_length=128,
        help_text="Only one roommate per room",
        null=True,
        blank=True,
    )
    dorm = models.CharField(
        "Reside in dorm",
        max_length=128,
        help_text="""
            Near teammates and/or friends&mdash;please be specific
            (player's names &amp; team name)
        """,
        null=True,
        blank=True,
    )
    # session
    session = models.CharField(
        choices=SESSIONS,
        max_length=128,
        help_text="<strong>Note</strong>: enrollment is limited.",
    )
    football = models.CharField(
        "Soccer ball",
        choices=BINARY_CHOICES,
        max_length=4,
        help_text="""
            <strong>Resident campers</strong>, please check here if you
            would like to purchase an official camp soccer ball for
            $30.00. Payment for ball and deposit must accompany
            application.
        """,
    )
    # payment
    reg_fee = models.CharField(
        "Registration Fee Total", max_length=7,
    )
    payment_method = models.CharField(
        choices=PAYMENT_CHOICES, max_length=24,
    )
    amount = models.CharField(
        "Amount to pay",
        choices=AMOUNT_CHOICES,
        max_length=24,
        help_text="NOTE: NO CREDIT CARDS ACCEPTED AT CHECK-INS",
    )
    # ancillary data
    medical_history = models.BooleanField(default=False)
    assumption_risk = models.BooleanField(default=False)
    insurance_card_front = models.FileField(
        max_length=768,
        upload_to="files/athletics/soccer-camp/insurance-cards",
        blank=True,
        null=True,
    )
    insurance_card_back = models.FileField(
        max_length=768,
        upload_to="files/athletics/soccer-camp/insurance-cards",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name_plural = 'Soccer Camp Attenders'


class SoccerCampBalance(Contact):
    """A model to save payments for the balance owed for registration."""

    registration = models.ForeignKey(SoccerCampAttender)
