from django.db import models
from djforms.core.models import Promotion, GenericContact
from django_countries import CountryField

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
    promotion           = models.ForeignKey(Promotion, null=True, blank=True)
    operator            = models.CharField(max_length=255, null=True, blank=True) # department etc
    total               = models.DecimalField(decimal_places=2, max_digits=10)
    comments            = models.TextField(null=True, blank=True)
    time_stamp          = models.DateTimeField("Timestamp", auto_now_add=True)
    status              = models.CharField("Status", max_length=20, choices=ORDER_STATUS, blank=True)
    auth                = models.CharField(max_length=16) # shop or store
    avs                 = models.BooleanField(default=False)
    cycle               = models.CharField(max_length=4, null=True, blank=True)
    payments            = models.IntegerField(null=True, blank=True)
    start_date          = models.DateField(null=True, blank=True)
    billingid           = models.CharField(max_length=100, null=True, blank=True)
    transid             = models.CharField(max_length=100, null=True, blank=True)

    def contact(self):
        return Contact.objects.get(order=self)

    def cid(self):
        return self.contact().id

    def first_name(self):
        return self.contact().first_name

    def last_name(self):
        return self.contact().last_name

    def email(self):
          return self.contact().email

    def __unicode__(self):
        c = Contact.objects.get(order=self)
        return u'%s %s' % (c.last_name, c.first_name)


class Contact(GenericContact):
    """
    Contact details for an order
    """
    second_name         = models.CharField(max_length=128, verbose_name="Middle name", null=True, blank=True)
    previous_name       = models.CharField(max_length=128, verbose_name="Previous name", null=True, blank=True)
    phone               = models.CharField(max_length=12, verbose_name='Phone number', help_text="Format: XXX-XXX-XXXX")
    address1            = models.CharField(max_length=255, verbose_name="Address")
    address2            = models.CharField(max_length=255, verbose_name="", null=True, blank=True)
    city                = models.CharField(max_length=128, verbose_name="City")
    state               = models.CharField(max_length=2, verbose_name="State")
    postal_code         = models.CharField(max_length=10, verbose_name="Zip")
    country             = CountryField(null=True, blank=True)
    order               = models.ManyToManyField(Order, related_name="contact_orders", null=True, blank=True)


