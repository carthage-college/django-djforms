# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from djtools.fields.helpers import upload_to_path


FORMATS = (
    ('Booklet / Event program','Booklet / Event program'),
    ('Brochure','Brochure'),
    ('Flyer / poster','Flyer / Poster'),
    ('Invitations','Invitations'),
    ('Multi-page book','Multi-page book'),
    ('Advertisement','Advertisement'),
    ('Postcard','Postcard'),
    ('Envelopes','Envelopes'),
    ('Other','Other')
)

CONSENT = (
    ('Yes','I agree'),
    ('NA','Mailing is not required')
)

WHO_MAILING = (
    ('Mail house','Mail house'),
    ('Requesting department','Requesting department'),
    ('Printer','Printer'),
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
        "Department phone number",
        max_length=21
    )
    account = models.CharField(
        "Account number",
        max_length=18, null=True, blank=True
    )
    sponsoring_department = models.CharField(
        "Sponsoring Department/Office",
        max_length=128, null=True, blank=True
    )
    contact_phone = models.CharField(
        "Contact phone number",
        max_length=21, null=True, blank=True,
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
    )
    target_audience = models.TextField(
        "Who is/are your target audience/audiences?",
        help_text = "For example: Alumni, prospective students, community.",
    )
    secondary_audience = models.TextField(
        "Are there secondary target audiences?",
        blank=True
    )
    print_format = models.CharField(
        "What is the format of your finished piece?",
        max_length=128,
        help_text="Check all that apply"
    )
    print_format_other = models.CharField(
        'If "Other" please describe',
        max_length=255,
        null=True, blank=True
    )
    approval = models.BooleanField(mark_safe(
        '''
        I am aware that all content appearing on campus must be
        approved by the Division of Student Affairs before hanging.
        I agree to review the
        <a href="/policies/" target="_blank">Event Promotion Policy</a>
        and adhere to those guidelines for this project.
        '''
    ))
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
        null=True, blank=True
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
        their established guidelines and procedures.
        Advancement requires two weeks lead time to produce
        a mail file. Requests can be submitted via the
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSexcu_M5TMphO4KpoKXNdchSzaeYWrjSHBoAKrL15M6YdtUGA/viewform">
        Advancement Office List Request Form
        </a>.
        """,
        max_length=128
    )
    website_update = models.CharField(
        "Is there a website that needs to be updated as part of this project?",
        max_length=4
    )
    website_url = models.CharField(
        "If so, what is the URL of the page that needs updating?",
        max_length=255,
        null=True,blank=True
    )
    is_mailing = models.CharField(
        "Is this project being mailed?",
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
    attachments = models.CharField(
        "Are you including attachments?",
        max_length=4
    )
    file_1 = models.FileField(
        "",
        upload_to=upload_to_path,
        blank=True
    )
    file_2 = models.FileField(
        "",
        upload_to=upload_to_path,
        blank=True
    )
    file_3 = models.FileField(
        "",
        upload_to=upload_to_path,
        blank=True
    )
    file_4 = models.FileField(
        "",
        upload_to=upload_to_path,
        blank=True
    )
    fact_checking = models.BooleanField(
        """
        I am responsible for fact-checking the spelling of names and titles,
        dates, times, locations, URLs, etc.
        """
    )
    lead_time = models.BooleanField(
        """
        I will provide adequate lead-time for each project and submit final and
        approved concepts, copy, and assets by the set deadlines.
        """
    )
    deadlines = models.BooleanField(
        """
        I understand that missing deadlines or making changes that result in
        more than two proofs will result in a delay of project completion date.
        """
    )

    class Meta:
        db_table = 'communications_printrequest'

    def get_slug(self):
        return 'files/communications/printrequest/'
