from django.db import models

class GenericPayment(models.Model):
    """
    A generic form to collect credit card information and the charge the credit card.
    """
    amount              = models.CharField(max_length=100, null=True, blank=True)
    cc_first_name       = models.CharField(max_length=100, verbose_name="First name on credit card", null=True, blank=True)
    cc_last_name        = models.CharField(max_length=100, verbose_name="Last name on credit card", null=True, blank=True)
    billing_address1    = models.CharField(max_length=255, verbose_name="Billing address", null=True, blank=True)
    billing_address2    = models.CharField(max_length=255, verbose_name="", null=True, blank=True)
    billing_city        = models.CharField(max_length=128, null=True, blank=True)
    billing_state       = models.CharField(max_length=2, null=True, blank=True)
    billing_postal_code = models.CharField(max_length=10, verbose_name="Billing zip", null=True, blank=True)
    card_number         = models.CharField(max_length=19, null=True, blank=True)
    expiration_month    = models.CharField(max_length=2, null=True, blank=True)
    expiration_year     = models.CharField(max_length=4, null=True, blank=True)
    security_code       = models.CharField(max_length=4, null=True, blank=True)
