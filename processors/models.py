from django.db import models
from djforms.core.models import Promotion

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

class Contact(models.Model):
    """
    Contact details for an order
    """
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    email       = models.EmailField()
    phone       = models.CharField(max_length=12, verbose_name='Phone Number', help_text="Format: XXX-XXX-XXXX")
    address1    = models.CharField(max_length=255, verbose_name="Address")
    address2    = models.CharField(max_length=255, verbose_name="", null=True, blank=True)
    city        = models.CharField(max_length=128, verbose_name="City")
    state       = models.CharField(max_length=2, verbose_name="State")
    postal_code = models.CharField(max_length=10, verbose_name="Zip")

    def __unicode__(self):
        return u'%s %s' % (self.last_name, self.first_name)

class Order(models.Model):
    """
    Orders contain a copy of all the information at the time the order was
    placed.
    """
    contact             = models.ForeignKey(Contact)
    promotion           = models.ForeignKey(Promotion, null=True, blank=True)
    total               = models.DecimalField(decimal_places=2, max_digits=10)
    time_stamp          = models.DateTimeField("Timestamp", auto_now_add=True)
    status              = models.CharField("Status", max_length=20, choices=ORDER_STATUS, blank=True)
    auth                = models.CharField(max_length=16) # shop or store
    avs                 = models.BooleanField(default=False)
    cycle               = models.CharField(max_length=4, null=True, blank=True)
    payments            = models.IntegerField(null=True, blank=True)
    start_date          = models.DateField(null=True, blank=True)
    billingid           = models.CharField(max_length=100, null=True, blank=True)
    transid             = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.contact.last_name, self.contact.first_name)

    def first_name(self):
        return self.contact.first_name

    def last_name(self):
        return self.contact.last_name

    def email(self):
        return self.contact.email

