from django.db import models
from djforms.processors.models import Contact

class DonationContact(Contact):
    """
    Donation contact details for an order
    """
    spouse = models.CharField(
        max_length=100, null=True, blank=True
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
