# -*- coding: utf-8 -*-

from django.db import models
from django.utils.safestring import mark_safe
from djtools.fields import BINARY_CHOICES
from localflavor.us.models import USStateField
from djforms.processors.models import Order


PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Check', 'Check'),
)
REGISTRATION_TYPES = (
    ('Regular Registration|520', 'Regular Registration'),
    ('Student Registration|300','Student Registration'),
    (
        'Montana Affiliate Registration|310',
        'Montana Affiliate Registration',
    ),
)
MEAL_CHOICES = (
    ('', '---select---'),
    ('Ham Sandwich', 'Ham Sandwich'),
    ('Turkey Sandwich', 'Turkey Sandwich'),
    ('Vegetable Sandwich', 'Vegetable Sandwich'),
)


class Activity(models.Model):
    """Conference registration data model for optional activities."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=64)
    price = models.CharField(max_length=64)
    meal = models.CharField(
        max_length=64,
        choices=MEAL_CHOICES,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'wsgc_registration_activity'


class Registration(models.Model):
    """Conference registration data model."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    suffix = models.CharField(max_length=128)
    full_name = models.CharField(
        "Full name exactly as you want it to appear on badge",
        max_length=128,
    )
    institution = models.CharField(
        "Consortium/Organization",
        max_length=128,
    )
    address1 = models.CharField(
        "Address",
        max_length=128,
    )
    address2 = models.CharField(
        "",
        max_length=128,
        null=True,
        blank=True,
    )
    city = models.CharField(max_length=128)
    state = USStateField(default='WI')
    postal_code = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(
        max_length=12,
        help_text="Format: XXX-XXX-XXXX",
    )
    registration_type = models.CharField(
        max_length=64,
        choices=REGISTRATION_TYPES,
    )
    dietary_restrictions = models.CharField(
        "Special Dietary Restrictions",
        max_length=255,
    )
    change_policy = models.BooleanField(
        default=False,
        verbose_name="I have read and agree to the Refund/Change Policy stated above.",
    )
    # payment
    payment_method = models.CharField(
        max_length=128,
        choices=PAYMENT_CHOICES
    )
    order = models.ForeignKey(
        Order,
        related_name='order',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'wsgc_registration_contact'


class Guest(models.Model):
    """Conference registration data model for guests."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_name = models.CharField(
        "Full name exactly as you want it to appear on badge",
        max_length=128,
    )
    registration = models.ForeignKey(
        Registration,
        verbose_name='Optional Activity',
        related_name='activity',
        on_delete=models.CASCADE,
    )
    tour = models.ForeignKey(
        Activity,
        verbose_name='Optional Activity',
        related_name='activity',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'wsgc_registration_guest'
