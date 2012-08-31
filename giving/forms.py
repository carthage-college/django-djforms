from django import forms

from djforms.processors.models import Order
from djforms.processors.forms import OrderForm

PAYMENT = (
    ('', '--------'),
    ('12', '1 year'),
    ('24', '2 years'),
    ('36', '3 years'),
    ('48', '4 years'),
    ('60', '5 years'),
)
CYCLES = (
    ('', '--------'),
    ('1m', 'Monthly'),
    ('3m', 'Quarterly'),
    ('12m', 'Yearly'),
)
class DonationOrderForm(OrderForm):
    """
    A donation form
    """

    class Meta:
        model = Order
        fields = ('total', 'cycle', 'payments', 'avs', 'start_date', 'auth')
        exclude = ('contact', 'time_stamp', 'status', 'billingid', 'transid','operator')


class SubscriptionOrderForm(OrderForm):
    """
    A subscrition form for recurring billing
    """
    payments            = forms.IntegerField(widget=forms.Select(choices=PAYMENT), max_value=60, min_value=12, label="Duration", help_text="Choose the number of years during which you want to donate the set amount above.")
    cycle               = forms.CharField(widget=forms.Select(choices=CYCLES), required=True, label="Interval", help_text="Choose how often the donation should be sent during the term of the pledge.")

    class Meta:
        model = Order
        fields = ('total', 'cycle', 'payments', 'avs', 'start_date', 'auth')
        exclude = ('contact', 'time_stamp', 'status', 'billingid', 'transid','operator')

