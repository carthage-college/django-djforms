from django import forms

from djforms.core.models import Promotion
from djforms.processors.models import Order
from djforms.processors.forms import ContactForm, OrderForm
from djforms.giving.models import BrickContact, DonationContact

from djtools.fields import TODAY
from djforms.core.models import BINARY_CHOICES

YEAR = TODAY.year
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
BRICK_TYPES = (
    (YEAR-2000+100,YEAR-2000+100),
    (250, 250),
    (YEAR-2000+300,YEAR-2000+300),
    (500, 500),
)
TOWER_INITITATIVE_BRICK_TYPES = (
    (500, 500),
    (1000, 1000)
)
RELATION_CHOICES = (
    ('', '--Select--'),
    ('Alumni', 'Alumni'),
    ('Employee', 'Employee'),
    ('Friend', 'Friend'),
    ('Parent', 'Parent'),
    ('Student', 'Student'),
)
CLASS = [(x, x) for x in reversed(xrange(1926,YEAR + 4))]
CLASS.insert(0, ('','-----'))


class BrickContactForm(ContactForm):
    """
    Brick contact form
    """

    class_of = forms.ChoiceField(
        required=False, label='Class of', choices=CLASS
    )
    brick_type = forms.ChoiceField(
        label='Class of', choices=BRICK_TYPES,
        widget=forms.RadioSelect()
    )
    inscription_1 = forms.CharField(
        max_length=14, required=False
    )
    inscription_2 = forms.CharField(
        max_length=14, required=False
    )
    inscription_3 = forms.CharField(
        max_length=14, required=False
    )
    inscription_4 = forms.CharField(
        max_length=14, required=False
    )
    inscription_5 = forms.CharField(
        max_length=14, required=False
    )

    class Meta:
        model = BrickContact
        fields = (
            'first_name','last_name','email','phone',
            'address1','address2','city','state','postal_code',
            'class_of','inscription_1','inscription_2','inscription_3',
            'inscription_4','inscription_5'
        )


class TowerInitiativeBrickContactForm(ContactForm):
    """
    Tower Initiative Brick contact form
    """

    class_of = forms.ChoiceField(
        required=False, label='Class of', choices=CLASS,
        help_text="If applicable"
    )
    brick_type = forms.ChoiceField(
        label='Class of', choices=TOWER_INITITATIVE_BRICK_TYPES,
        widget=forms.RadioSelect()
    )
    inscription_1 = forms.CharField(
        max_length=19, required=False
    )
    inscription_2 = forms.CharField(
        max_length=19, required=False
    )
    inscription_3 = forms.CharField(
        max_length=19, required=False
    )
    inscription_4 = forms.CharField(
        max_length=19, required=False
    )
    inscription_5 = forms.CharField(
        max_length=19, required=False
    )
    inscription_6 = forms.CharField(
        max_length=19, required=False
    )
    inscription_7 = forms.CharField(
        max_length=19, required=False
    )

    class Meta:
        model = BrickContact
        fields = (
            'first_name','last_name','email','phone',
            'address1','address2','city','state','postal_code',
            'class_of','inscription_1','inscription_2','inscription_3',
            'inscription_4','inscription_5','inscription_6','inscription_7'
        )


class BrickOrderForm(OrderForm):
    """
    Brick order form
    """

    total = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Order
        fields = ('total','avs','auth')


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
    anonymous = forms.BooleanField(
        required=False,
        label='''
            I would like my gift to remain anonymous, and not be
            published on any donor list or in the annual report.
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
        '''
        fields = (
            'first_name','last_name','relation','class_of','email',
            'address1','address2','city','state','postal_code','opt_in',
            'anonymous'
        )
        '''
        fields = (
            'first_name','last_name','spouse','relation','class_of','email',
            'phone','address1','address2','city','state','postal_code',
            'matching_company','opt_in','anonymous'
        )


class GivingDayDonationContactForm(DonationContactForm):
    """
    Giving Day campaign form, extends Donation Contact form
    """

    def __init__(self, *args, **kwargs):
        super(GivingDayDonationContactForm, self).__init__(*args, **kwargs)
        self.fields.pop('phone')
        self.fields.pop('spouse')
        self.fields.pop('opt_in')

    class Meta:
        model = DonationContact
        fields = (
            'first_name','last_name','relation','class_of','email',
            'address1','address2','city','state','postal_code','opt_in',
            'anonymous'
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
    payments = forms.CharField(
        required=False, widget=forms.HiddenInput()
    )
    pledge = forms.CharField(
        required=False, widget=forms.HiddenInput()
    )

    class Meta:
        model = Order
        fields = ('total','comments','avs','auth','payments')


class PledgeContactForm(DonationContactForm):
    """
    Pledge Contact form, inherits everything from DonationContactForm and
    is merely a placeholder for view logic
    """
    pass


class GivingDayPledgeContactForm(DonationContactForm):
    """
    Same as above, but for Giving Day
    """
    pass


class PledgeOrderForm(OrderForm):
    """
    A subscrition form for recurring billing
    """
    total = forms.CharField(
        label="Gift installments",
        help_text="How much would you like to give for each installment."
    )
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
        label="Frequency",
        help_text='''
            Choose how often the donation should be sent during the term
            of the pledge.
        '''
    )

    class Meta:
        model = Order
        fields = (
            'total', 'cycle', 'payments', 'comments', 'avs',
            'auth'
        )

class ManagerContactForm(DonationContactForm):
    '''
    form that allows manager to create a donation contact manually for
    things like cash donations
    '''

    first_name = forms.CharField(
        max_length=128, required=False
    )
    email = forms.EmailField(
        label = "Your email address",
        required = False,
        max_length=128
    )

    def __init__(self, *args, **kwargs):
        super(ManagerContactForm, self).__init__(*args, **kwargs)
        self.fields.pop('state')
        self.fields.pop('postal_code')
        self.fields.pop('phone')
        self.fields.pop('spouse')
        self.fields.pop('opt_in')
        self.fields.pop('matching_company')

    class Meta:
        model = DonationContact
        fields = (
            'first_name','last_name','relation','class_of','email'
        )


class ManagerOrderForm(forms.ModelForm):
    """
    form that allows manager to create a donation order manually for
    things like cash donations
    """
    promotion = forms.ModelChoiceField(
        label = "Promotion",
        queryset = Promotion.objects.all().order_by('-date_created'),
        required = False
    )
    '''
    opt_in = forms.CharField(widget=forms.HiddenInput())
    anonymous = forms.CharField(widget=forms.HiddenInput())
    matching_company = forms.CharField(widget=forms.HiddenInput())
    '''

    class Meta:
        model = Order
        fields = ('total','promotion')

