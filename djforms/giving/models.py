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

    def order_cc_name(self):
        try:
            name = self.order.all()[0].cc_name
        except:
            name = None
        return name

    def order_promo(self):
        try:
            promo = self.order.all()[0].promotion
        except:
            promo = None
        return promo

    def order_status(self):
        try:
            stat = self.order.all()[0].status
        except:
            stat = None
        return stat

    def order_oid(self):
        try:
            oid = self.order.all()[0].id
        except:
            oid = None
        return oid

    def order_transid(self):
        try:
            tid = self.order.all()[0].transid
        except:
            tid = None
        return tid

    def order_total(self):
        try:
            tid = self.order.all()[0].total
        except:
            tid = None
        return tid

    def order_cycle(self):
        try:
            cycle = self.order.all()[0].cycle
        except:
            cycle = None
        return cycle

    def order_payments(self):
        try:
            payments = self.order.all()[0].payments
        except:
            payments = None
        return payments

    def order_start_date(self):
        try:
            sdate = self.order.all()[0].start_date
        except:
            sdate = None
        return sdate

    def order_comments(self):
        try:
            com = self.order.all()[0].comments
        except:
            com = None
        return com

    def order_statement(self):
        try:
            sta = self.order.all()[0].statement
        except:
            sta = None
        return sta

    def order_binary(self):
        try:
            bny = self.order.all()[0].binary
        except:
            bny = None
        return bny


class PaverContact(Contact):
    '''
    Paver contact details for an order
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

    def order_cc_name(self):
        try:
            name = self.order.all()[0].cc_name
        except:
            name = None
        return name

    def order_promo(self):
        try:
            promo = self.order.all()[0].promotion
        except:
            promo = None
        return promo

    def order_status(self):
        try:
            stat = self.order.all()[0].status
        except:
            stat = None
        return stat

    def order_transid(self):
        try:
            tid = self.order.all()[0].transid
        except:
            tid = None
        return tid

    def order_total(self):
        try:
            tid = self.order.all()[0].total
        except:
            tid = None
        return tid

    def order_cycle(self):
        try:
            cycle = self.order.all()[0].cycle
        except:
            cycle = None
        return cycle

    def order_payments(self):
        try:
            payments = self.order.all()[0].payments
        except:
            payments = None
        return payments

    def order_start_date(self):
        try:
            sdate = self.order.all()[0].start_date
        except:
            sdate = None
        return sdate

    def order_comments(self):
        try:
            com = self.order.all()[0].comments
        except:
            com = None
        return com
