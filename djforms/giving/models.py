from django.db import models
from django.contrib.auth.models import User

from djforms.processors.models import Contact


class DonationContact(Contact):
    '''
    Donation contact details for an order
    '''

    spouse = models.CharField(
        max_length=100,
        null=True, blank=True
    )
    relation = models.CharField(
        max_length=100,
        verbose_name="Relation to Carthage",
        null=True, blank=True
    )
    class_of = models.CharField(
        max_length=4, null=True, blank=True
    )
    matching_company = models.BooleanField(
        verbose_name='I/we are employed by a matching gift company.'
    )
    opt_in = models.BooleanField(
        verbose_name='''
            I would like more information about planned gifts such as
            charitable trusts, charitable gifts annuities, life insurance,
            or will inclusions.
        '''
    )
    anonymous = models.BooleanField(
        verbose_name='''
            I would like my gift to remain anonymous, and not be
            published on any donor list or in the annual report.
        '''
    )


class BrickContact(Contact):
    '''
    Brick contact details for an order
    '''

    class_of = models.CharField(
        max_length=4, null=True, blank=True
    )
    inscription_1 = models.CharField(
        max_length=24
    )
    inscription_2 = models.CharField(
        max_length=24
    )
    inscription_3 = models.CharField(
        max_length=24
    )
    inscription_4 = models.CharField(
        max_length=24, null=True, blank=True
    )
    inscription_5 = models.CharField(
        max_length=24, null=True, blank=True
    )
    inscription_6 = models.CharField(
        max_length=24, null=True, blank=True
    )
    inscription_7 = models.CharField(
        max_length=24, null=True, blank=True
    )
