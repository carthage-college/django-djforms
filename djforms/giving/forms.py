from django import forms

from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.giving.models import DonationContact

from datetime import date

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
RELATION_CHOICES = (
    ('', '--Select--'),
    ('Alumni', 'Alumni'),
    ('Employee', 'Employee'),
    ('Friend', 'Friend'),
    ('Parent', 'Parent'),
    ('Student', 'Student'),
)
CLASS = [(x, x) for x in reversed(xrange(1926,date.today().year + 4))]
CLASS.insert(0, ("","-----"))

class DonationContactForm(ContactForm):
    """
    Donation Contact form, extends base ContactForm in processors app
    """
    class_of = forms.ChoiceField(
        required=False, label='Class of', choices=CLASS
    )
    matching_company = forms.BooleanField(
        required=False,
        label='I/we are employed by a matching gift company.'
    )
    opt_in = forms.BooleanField(
        required=False,
        label='''
            I would like more information about planned gifts such as
            charitable trusts, charitable gifts annuities,
            life insurance, or will inclusions.
        '''
    )
    spouse = forms.CharField(
        required=False, label='Spouse', max_length=100
    )
    relation = forms.ChoiceField(
        choices=RELATION_CHOICES, label='Relation to Carthage'
    )

    class Meta:
        model = DonationContact
        fields = (
            'first_name','last_name','spouse','relation','class_of','email',
            'phone','address1','address2','city','state','postal_code',
            'matching_company','opt_in'
        )

class DonationOrderForm(OrderForm):
    """
    A donation form
    """

    total = forms.CharField(label="Amount")
    comments = forms.CharField(
        label = "Designation",
        help_text='''
            Please indicate if you would like your gift to be directed to
            a specific area. If this space is left blank, gifts will be
            directed to the
            <a href="/give/carthage-fund/">Carthage Fund</a>.
        ''',
        required=False
    )

    class Meta:
        model = Order
        fields = ('total','comments','avs','auth')
        #fields = ('total','avs','auth')

class PledgeOrderForm(OrderForm):
    """
    A subscrition form for recurring billing
    """
    total = forms.CharField(label="Amount")
    comments = forms.CharField(
        label = "Designation",
        help_text = '''
            Please indicate if you would like your gift to be directed to
            a specific area. If this space is left blank, gifts will be
            directed to the
            <a href="/give/carthage-fund/">Carthage Fund</a>.
        ''',
        required=False
    )
    payments = forms.IntegerField(
        widget=forms.Select(choices=PAYMENT),
        max_value=60, min_value=12, label="Duration",
        help_text='''
            Choose the number of years during which you want to donate
            the set amount above.
        '''
    )
    cycle = forms.CharField(
        widget=forms.Select(choices=CYCLES),
        required=True,
        label="Interval",
        help_text='''
            Choose how often the donation should be sent during the term
            of the pledge.
        '''
    )

    class Meta:
        model = Order
        fields = (
            'total', 'comments', 'cycle', 'payments', 'avs',
            'start_date', 'auth'
        )
