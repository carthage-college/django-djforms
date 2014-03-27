from django.db import models
from django.core import urlresolvers
from django.utils.safestring import mark_safe

from django_countries import CountryField
from djforms.core.models import Promotion, GenericContact

ORDER_STATUS = (
    ('Blocked', 'Blocked'),
    ('In process', 'In process'),
    ('Pay later', 'Pay later'),
    ('Cancelled', 'Cancelled'),
    ('approved', 'Approved'),
    ('accepted', 'Accepted'),
    ('decline', 'Decline'),
    ('baddata', 'Bad data'),
    ('error', 'Error'),
)

class Order(models.Model):
    """
    Orders contain a copy of all the information at the time the order was
    placed.
    """
    cc_name             = models.CharField(max_length=255, null=True, blank=True)
    cc_4_digits         = models.CharField(max_length=4, null=True, blank=True)
    promotion           = models.ForeignKey(Promotion, null=True, blank=True)
    operator            = models.CharField(max_length=255, null=True, blank=True) # department etc
    total               = models.DecimalField(decimal_places=2, max_digits=10)
    comments            = models.TextField(null=True, blank=True)
    time_stamp          = models.DateTimeField("Timestamp", auto_now_add=True)
    export_date         = models.DateTimeField(blank=True,null=True)
    status              = models.CharField("Status", max_length=20, choices=ORDER_STATUS, blank=True)
    auth                = models.CharField(max_length=16) # shop or store
    avs                 = models.BooleanField(default=False)
    cycle               = models.CharField(max_length=4, null=True, blank=True)
    payments            = models.IntegerField(null=True, blank=True)
    start_date          = models.DateField(null=True, blank=True)
    billingid           = models.CharField(max_length=100, null=True, blank=True)
    transid             = models.CharField(max_length=100, null=True, blank=True)

    def contact(self):
        try:
            cs = Contact.objects.filter(order=self).order_by('id')[0]
        except:
            cs = None
        return cs

    def cid(self):
        try:
            cid = self.contact().id
        except:
            cid = None
        return cid

    def first_name(self):
        try:
            fn = self.contact().first_name
        except:
            fn = None
        return fn

    def last_name(self):
        try:
            ln = self.contact().last_name
        except:
            ln = None
        return ln

    def email(self):
        try:
            e = self.contact().email
        except:
            e = None
        return e

    def __unicode__(self):
        try:
            c = Contact.objects.get(order=self)
            return u'%s %s' % (c.last_name, c.first_name)
        except:
            return ""

class Contact(GenericContact):
    """
    Contact details for an order
    """
    second_name         = models.CharField(max_length=128, verbose_name="Middle name", null=True, blank=True)
    previous_name       = models.CharField(max_length=128, verbose_name="Previous name", null=True, blank=True)
    salutation          = models.CharField(max_length=16, null=True, blank=True)
    phone               = models.CharField(max_length=12, verbose_name='Phone number', help_text="Format: XXX-XXX-XXXX")
    address1            = models.CharField(max_length=255, verbose_name="Address", null=True, blank=True)
    address2            = models.CharField(max_length=255, verbose_name="", null=True, blank=True)
    city                = models.CharField(max_length=128, verbose_name="City", null=True, blank=True)
    state               = models.CharField(max_length=2, verbose_name="State", null=True, blank=True)
    postal_code         = models.CharField(max_length=10, verbose_name="Zip", null=True, blank=True)
    country             = CountryField(null=True, blank=True)
    order               = models.ManyToManyField(Order, related_name="contact_orders", null=True, blank=True)
    #longitude           = models.DecimalField(max_digits=9, decimal_places=6, null=True,blank=True)
    #latitude            = models.DecimalField(max_digits=9, decimal_places=6, null=True,blank=True)

