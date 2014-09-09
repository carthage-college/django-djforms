# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from djtools.fields import BINARY_CHOICES

FORMATS = (
    ('Booklet / Event program','Booklet / Event program'),
    ('Brochure','Brochure'),
    ('Flyer / poster','Flyer / Poster'),
    ('Invitations','Invitations'),
    ('Multi-page book','Multi-page book'),
    ('Advertisement','Advertisement'),
    ('Postcard','Postcard'),
    ('Other','Other')
)

CONSENT = (
    ('yes','I agree'),
    ('na','Mailing is not required')
)

WHO_MAILING = (
    ('Mail house','Mail house'),
    ('Requesting department','Requesting department'),
    ('None','None')
)

HOW_MAILING = (
    ('Self mailer','Self mailer'),
    ('I need envelopes','I need envelopes'),
    ('I have envelopes','I have envelopes'),
    ('None','None')
)

SPEED_MAILING = (
    ('1st Class','1st Class'),
    ('Non-profit / Bulk','Non-profit / Bulk'),
    ('None','None')
)

class PrintRequest(models.Model):
    user = models.ForeignKey(
        User, verbose_name="Created by",
        related_name="communications_print_request_user",
        editable=False
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="communications_print_request_updated_by",
        editable=False
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        "Date Updated", auto_now=True
    )
    department = models.CharField(
        "Department",
        max_length=128
    )
    phone = models.CharField(
        "Phone number",
        max_length=12
    )
    account = models.CharField(
        "Account number",
        max_length=18
    )
    estimate = models.BooleanField(
        "Do you require an estimate for this project before we begin?",
        help_text = "Please allow an additional 48-72 hours to deliver quotes."
    )
    project_name = models.CharField(
        "What is the name of your project?",
        max_length=128
    )
    project_purpose = models.TextField(
        "Briefly describe the purpose of your request",
        max_length=128
    )
    target_audience = models.TextField(
        "Who is/are your target audience/audiences?",
        help_text = "For example: Alumni, prospective students, community.",
        max_length=128
    )
    secondary_audience = models.TextField(
        "Are there secondary target audiences?",
        max_length=128,
        blank=True
    )
    print_format = models.CharField(
        "What is the format of your finished piece?",
        max_length=128,
        help_text="Check all that apply"
    )
    print_format_other = models.CharField(
        "If 'Other' please describe",
        max_length=128
    )
    format_quantity = models.CharField(
        "What is the quantity for each format?",
        max_length=128
    )
    special_instructions = models.TextField(
        """
        Please provide a short description -
        including special instructions -
        needed for each item you selected above.
        """,
        max_length=128
    )
    delivery_date = models.DateField(
        "Final requested delivery date of project",
        auto_now=False
    )
    consent = models.CharField(
        """
        If the Office of Communications coordinates
        your mailing with a mail house, we need your
        mailing list at least one week before the mail
        date. It is your responsibility to coordinate
        the request from Institutional Advancement within
        their established guidelines and procedures
        """,
        choices=CONSENT,
        max_length=128
    )
    is_mailing = models.CharField(
        "Is this project being mailed?",
        choices=BINARY_CHOICES,
        max_length=4
    )
    who_mailing = models.CharField(
        "Who is mailing?",
        choices=WHO_MAILING,
        blank=True,
        max_length=128
    )
    how_mailing = models.CharField(
        "How is it being mailed?",
        choices=HOW_MAILING,
        blank=True,
        max_length=128
    )
    speed_mailing = models.CharField(
        "Please indicate how your piece is to be mailed",
        choices=SPEED_MAILING,
        blank=True,
        max_length=128
    )
    using_attachments = models.CharField(
        "Are you including attachments?",
        choices=BINARY_CHOICES,
        max_length=4
    )
    file_1 = models.FileField(
        "",
        upload_to="files/communications/printrequest/",
        blank=True
    )
    file_2 = models.FileField(
        "",
        upload_to="files/communications/printrequest/",
        blank=True
    )
    file_3 = models.FileField(
        "",
        upload_to="files/communications/printrequest/",
        blank=True
    )
    file_4 = models.FileField(
        "",
        upload_to="files/communications/printrequest/",
        blank=True
    )

    class Meta:
        db_table = 'communications_printrequest'
