from django.db import models
from django.contrib.auth.models import User

from djforms.processors.models import Contact


class DonationContact(Contact):
    """Donation contact details for an order."""

    COLUMNS = {
        0: 'last_name',
        1: 'first_name',
        2: 'order_cc_name',
        3: 'created_at',
        4: 'email',
        5: 'twitter',
        6: 'phone',
        7: 'address',
        8: 'city',
        9: 'state',
        10: 'postal_code',
        11: 'spouse',
        12: 'relation',
        13: 'honouring',
        14: 'class_of',
        15: 'order_promo',
        16: 'order_transid',
        17: 'order_status',
        18: 'order_total',
        19: 'order_comments',
        20: 'anonymous',
        21: 'hidden',
    }

    honouring = models.CharField(
        "In Honor Of",
        max_length=254,
        null=True,
        blank=True,
    )
    endowment = models.CharField(
        "Specific endowed scholarship and athletic team designations",
        max_length=254,
        null=True,
        blank=True,
    )
    spouse = models.CharField(
        "Spouse full name",
        max_length=100,
        null=True,
        blank=True,
    )
    spouse_class = models.CharField(
        "Spouse's Class",
        max_length=4,
        null=True,
        blank=True,
    )
    relation = models.CharField(
        "Relation to Carthage",
        max_length=100,
        null=True,
        blank=True,
    )
    class_of = models.CharField(max_length=4, null=True, blank=True)
    matching_company = models.BooleanField(
        verbose_name="I/we are employed by a matching gift company.",
    )
    opt_in = models.BooleanField(
        verbose_name="""
            I would like more information about planned gifts such as
            charitable trusts, charitable gifts annuities, life insurance,
            or will inclusions.
        """,
    )
    anonymous = models.BooleanField(
        verbose_name="""
            I would like my gift to remain anonymous, and not be
            published on any donor list or in the annual report.
        """,
    )
    hidden = models.BooleanField()
    twitter = models.CharField(
        "Twitter Handle",
        max_length=128,
        null=True,
        blank=True,
    )

    def order_cc_name(self):
        """Return the name on the credit card."""
        try:
            name = self.order.all().first().cc_name
        except:
            name = None
        return name

    def order_promo(self):
        """Return the promotion with which this transaction was associated."""
        try:
            promo = self.order.all().first().promotion
        except:
            promo = None
        return promo

    def order_status(self):
        """Return the status of the order."""
        try:
            stat = self.order.all().first().status.lower()
        except:
            stat = None
        return stat

    def order_oid(self):
        """Return the ID of the order."""
        try:
            oid = self.order.all().first().id
        except:
            oid = 0
        return oid

    def order_transid(self):
        """Return the transaction ID from the credit card processor."""
        try:
            tid = self.order.all().first().transid
        except:
            tid = None
        return tid

    def order_total(self):
        """Return the order total."""
        try:
            tid = self.order.all().first().total
        except:
            tid = None
        return tid

    def order_cycle(self):
        """Return the recurring payment cycle."""
        try:
            cycle = self.order.all().first().cycle
        except:
            cycle = None
        return cycle

    def order_payments(self):
        """Return the payments type."""
        try:
            payments = self.order.all().first().payments
        except:
            payments = None
        return payments

    def order_start_date(self):
        """Return the start date for recurring payments."""
        try:
            sdate = self.order.all().first().start_date
        except:
            sdate = None
        return sdate

    def order_comments(self):
        """Return the comments on a transaction."""
        try:
            com = self.order.all().first().comments
        except:
            com = None
        return com

    def order_statement(self):
        """Return the statment."""
        try:
            sta = self.order.all().first().statement
        except:
            sta = None
        return sta

    def order_binary(self):
        """Return the binary value."""
        try:
            bny = self.order.all().first().binary
        except:
            bny = None
        return bny


class PaverContact(Contact):
    """Paver contact details for an order."""

    class_of = models.CharField(
        max_length=4,
        null=True,
        blank=True,
    )
    inscription_1 = models.CharField(max_length=24)
    inscription_2 = models.CharField(max_length=24)
    inscription_3 = models.CharField(max_length=24)
    inscription_4 = models.CharField(max_length=24, null=True, blank=True)
    inscription_5 = models.CharField(max_length=24, null=True, blank=True)
    inscription_6 = models.CharField(max_length=24, null=True, blank=True)
    inscription_7 = models.CharField(max_length=24, null=True, blank=True)

    def order_cc_name(self):
        """Return the name on the credit card."""
        try:
            name = self.order.all().first().cc_name
        except:
            name = None
        return name

    def order_promo(self):
        """Return the promotion with which this transaction was associated."""
        try:
            promo = self.order.all().first().promotion
        except:
            promo = None
        return promo

    def order_status(self):
        """Return the status of the order."""
        try:
            stat = self.order.all().first().status
        except:
            stat = None
        return stat

    def order_transid(self):
        """Return the transaction ID from the credit card processor."""
        try:
            tid = self.order.all().first().transid
        except:
            tid = None
        return tid

    def order_total(self):
        """Return the order total."""
        try:
            tid = self.order.all().first().total
        except:
            tid = None
        return tid

    def order_cycle(self):
        """Return the recurring payment cycle."""
        try:
            cycle = self.order.all().first().cycle
        except:
            cycle = None
        return cycle

    def order_payments(self):
        """Return the payments type."""
        try:
            payments = self.order.all().first().payments
        except:
            payments = None
        return payments

    def order_start_date(self):
        """Return the start date for recurring payments."""
        try:
            sdate = self.order.all().first().start_date
        except:
            sdate = None
        return sdate

    def order_comments(self):
        """Return the comments on a transaction."""
        try:
            com = self.order.all().first().comments
        except:
            com = None
        return com
