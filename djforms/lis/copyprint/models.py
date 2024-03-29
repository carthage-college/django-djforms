# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


STATUS = (
    ("New", "New"),
    ("Replacement", "Replacement"),
)


class CardRequest(models.Model):

    user = models.ForeignKey(
        User, verbose_name="Created by",
        related_name="copyprint_card_request_user",
        on_delete=models.CASCADE,
        editable=False,
    )
    updated_by = models.ForeignKey(
        User, verbose_name="Updated by",
        related_name="copyprint_card_request_updated_by",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        editable=False,
    )
    date_created = models.DateTimeField(
        "Date Created", auto_now_add=True
    )
    date_updated = models.DateTimeField(
        null=True, blank=True, auto_now=True,
        editable=False
    )
    #core
    entity_name = models.CharField(
        max_length=128,
        help_text = "The department, organization, or club name"
    )
    account_number = models.CharField(
        max_length=16
    )
    entity_head = models.CharField(
        "The department head or the entity's president",
        max_length=128
    )
    entity_treasurer = models.CharField(
        "Treasurer or equivalent",
        max_length=128,
        null=True, blank=True,
    )
    entity_advisor = models.CharField(
        "Advisor",
        max_length=128,
        null=True, blank=True
    )
    printing_budget = models.CharField(
        "Printing Budget Amount",
        max_length=16,
        null=True, blank=True
    )
    status = models.CharField(
        "What type of card are you requesting?",
        max_length=32,
        choices=STATUS
    )

    class Meta:
        db_table = 'lis_copyprint_card_request'

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email

    def get_fields(self):
        return [
            (field.name, field.value_to_string(self)) for field in CardRequest._meta.fields
        ]

    def __str__(self):
        return "{0}, {1} from {2}".format(
            self.user.last_name,
            self.user.first_name,
            self.entity_name,
        )
