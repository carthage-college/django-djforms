'''
Notes for steve:

 1. Do we have a phone field?
'''

from django.db import models
from django.conf import settings

from djtools.fields import BINARY_CHOICES

FORMATS = (
    ('booklet event','Booklet / Event program'),
    ('brochure','Brochure'),
    ('flyer poster','Flyer / Poster'),
    ('invitations','Invitations'),
    ('multpage','Multi-page book'),
    ('advertisement','Advertisement'),
    ('postcard','Postcard')
)

CONSENT = (
    ('yes','I agree'),
    ('na','Mailing is not required')
)

WHO_MAILING = (
    ('mail house','Mail house'),
    ('department','Requesting department'),
    ('none','None')
)

HOW_MAILING = (
    ('self mailer','Self mailer'),
    ('envelopes','I need envelopes'),
    ('have envelopes','I already have envelopes'),
    ('none','None')
)

SPEED_MAILING = (
    ('first','1st Class'),
    ('bulk','Non-profit/Bulk'),
    ('none','None')
)

class PrintRequest(models.Model):

    name = models.CharField(
        "Name",
        max_length=128
    )
    department = models.CharField(
        "Department",
        max_length=128
    )
    phone = models.CharField(
        "Phone number",
        max_length=16
    )
    email = models.EmailField(
        "Email"
    )
    account = models.IntegerField(
        "Account number"
    )
    estimate = models.BooleanField(
        """
        Do you require an estimate for this project before we begin?
        (Please allow an additional 48-72 hours to deliver quotes.)
        """
    )
    project_name = models.CharField(
        "What is the name of your project",
        max_length=128
    )
    project_purpose = models.CharField(
        "Briefly describe the purpose of your request",
        max_length=128
    )
    target_audience = models.CharField(
        """
        Who is/are your target audience/audiences?
        (For example: Alumni, prospective students, community.)
        """,
        max_length=128
    )
    secondary_audience = models.CharField(
        "Are there secondary target audiences",
        max_length=128,
        blank=True
    )
    print_format = models.CharField(
        "What is the format of your finished piece",
        choices=FORMATS
    )
    format_quantity = models.CharField(
        "What is the quantity for each format",
        max_length=128
    )
    special_instructions = models.CharField(
        """
        Please provide a short description -
        including special instructions -
        needed for each item you selected above.
        """,
        max_length=128
    )
    delivery_date = models.CharField(
        "Final requested delivery date of project",
        max_length=20
    )
    delivery_location = models.CharField(
        """
        Final requested delivery location:
        (Please include the full name of your office,
        office room number, and name of recipient.)
        """,
        max_length=128
    )
    delivery_instructions = models.CharField(
        "Delivery instructions",
        max_length=128
    )
    consent = models.CharField(
        "If the Office of Communications coordinates \
        your mailing with a mail house, we need your \
        mailing list at least one week before the mail \
        date. It is your responsibility to coordinate \
        the request from Institutional Advancement within \
        their established guidelines and procedures",
        choices=CONSENT
    )
    is_mailing = models.CharField(
        "Is this project being mailed",
        choices=BINARY_CHOICES
    )
    who_mailing = models.CharField(
        "Who is mailing",
        choices=WHO_MAILING,
        blank=True
    )
    how_mailing = models.CharField(
        "How is it being mailed",
        choices=HOW_MAILING,
        blank=True
    )
    speed_mailing = models.CharField(
        "Please indicate how your piece is to be mailed",
        choices=SPEED_MAILING,
        blank=True
    )
    file_1 = models.FileField(
        "File 1",
        blank=True
    )
    file_2 = models.FileField(
        "File 2",
        blank=True
    )
    file_3 = models.FileField(
        "File 3",
        blank=True
    )
    file_4 = models.FileField(
        "File 4",
        blank=True
    )
