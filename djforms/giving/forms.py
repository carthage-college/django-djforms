# -*- coding: utf-8 -*-

from django import forms

from djforms.core.models import Promotion
from djforms.core.models import STATE_CHOICES
from djforms.processors.models import Order
from djforms.processors.forms import ContactForm
from djforms.processors.forms import OrderForm
from djforms.giving.models import DonationContact
from djforms.giving.models import PaverContact
from djtools.fields import TODAY
from djforms.core.models import BINARY_CHOICES

YEAR = TODAY.year
MILLENNIUM = 2000
if TODAY.month < 9:
    MILLENNIUM += 1
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
PAVER_TYPES = (
    (YEAR-MILLENNIUM+180.21,YEAR-MILLENNIUM+180.21),
    (250, 250),
    (YEAR-MILLENNIUM+400.21,YEAR-MILLENNIUM+400.21),
    (500, 500),
    (YEAR-MILLENNIUM+800.21,YEAR-MILLENNIUM+800.21),
    (1000, 1000),
)
RELATION_CHOICES = (
    ('', '--Select--'),
    ('Alumni', 'Alumni'),
    ('Employee', 'Employee'),
    ('Friend', 'Friend'),
    ('Parent', 'Parent'),
    ('Student', 'Student'),
)
CLASS = [(x, x) for x in reversed(range(1926, YEAR + 4))]
CLASS.insert(0, ('', '-----'))


class PhotoCaptionForm(forms.Form):
    """Add a caption to a photo form."""

    caption1 = forms.CharField(max_length=13, required=False)
    caption2 = forms.CharField(max_length=13, required=False)
    caption3 = forms.CharField(max_length=13, required=False)


class PaverContactForm(ContactForm):
    """Paver contact form."""

    class_of = forms.ChoiceField(
        label='Class of',
        required=False,
        choices=CLASS,
        help_text="If applicable",
    )
    paver_type = forms.ChoiceField(
        label='Class of',
        choices=PAVER_TYPES,
        widget=forms.RadioSelect(),
    )
    inscription_1 = forms.CharField(required=False)
    inscription_2 = forms.CharField(required=False)
    inscription_3 = forms.CharField(required=False)
    inscription_4 = forms.CharField(required=False)
    inscription_5 = forms.CharField(required=False)
    inscription_6 = forms.CharField(required=False)
    inscription_7 = forms.CharField(required=False)

    class Meta:
        model = PaverContact
        fields = (
            'first_name',
            'last_name',
            'email',
            'phone',
            'address1',
            'city',
            'state',
            'postal_code',
            'class_of',
            'inscription_1',
            'inscription_2',
            'inscription_3',
            'inscription_4',
            'inscription_5',
            'inscription_6',
            'inscription_7',
        )


class PaverOrderForm(OrderForm):
    """Paver order form."""

    total = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Order
        fields = ('total', 'avs', 'auth')


class DonationContactForm(ContactForm):
    """Donation Contact form, extends base ContactForm in processors app."""

    address1 = forms.CharField(
        label="Address",
        required=True,
    )
    city = forms.CharField()
    state = forms.ChoiceField(required=True, choices=STATE_CHOICES)
    postal_code = forms.CharField(required=True)
    class_of = forms.ChoiceField(label='Class of', required=False, choices=CLASS)
    matching_company = forms.BooleanField(
        label='I/we are employed by a matching gift company',
        required=False,
    )
    opt_in = forms.BooleanField(
        label='''
            I would like more information about planned gifts such as
            charitable trusts, charitable gifts annuities,
            life insurance, or will inclusions.
        ''',
        required=False,
    )
    anonymous = forms.BooleanField(
        label='''
            I would like my gift to remain anonymous, and not be
            published on any donor list or in the annual report.
        ''',
        required=False,
    )
    spouse_class = forms.ChoiceField(
        label="Spouse's Class",
        choices=CLASS,
        required=False,
    )
    relation = forms.ChoiceField(
        label='Relation to Carthage',
        choices=RELATION_CHOICES,
    )

    class Meta:
        model = DonationContact
        fields = (
            'honouring',
            'first_name',
            'last_name',
            'class_of',
            'relation',
            'spouse',
            'spouse_class',
            'email',
            'phone',
            'address1',
            'city',
            'state',
            'postal_code',
            'matching_company',
            'opt_in',
            'anonymous',
        )


class CarthageCampaignDonationContactForm(DonationContactForm):
    """Giving Day campaign form, extends Donation Contact form."""

    def __init__(self, *args, **kwargs):
        super(CarthageCampaignDonationContactForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DonationContact
        fields = (
            'endowment',
            'honouring',
            'first_name',
            'last_name',
            'spouse',
            'spouse_class',
            'relation',
            'class_of',
            'email',
            'phone',
            'address1',
            'city',
            'state',
            'postal_code',
            'matching_company',
            'opt_in',
            'anonymous',
        )


class GivingDayDonationContactForm(DonationContactForm):
    """Giving Day campaign form, extends Donation Contact form."""

    def __init__(self, *args, **kwargs):
        super(GivingDayDonationContactForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DonationContact
        fields = (
            'first_name',
            'last_name',
            'relation',
            'class_of',
            'spouse',
            'spouse_class',
            'email',
            'phone',
            'twitter',
            'address1',
            'city',
            'state',
            'postal_code',
            'opt_in',
            'anonymous',
        )


class DonationOrderForm(OrderForm):
    """A donation form."""

    total=forms.CharField(label="Amount")
    comments=forms.CharField(
        label='Designation',
        help_text='''
            Please indicate if you would like your gift to be directed to a specific area.
            If you do not have a specific designation in mind,
            please enter "n/a" and we'll use your gift where it's needed most!
        ''',
    )
    comments_other=forms.CharField(required=False)
    payments = forms.CharField(required=False, widget=forms.HiddenInput())
    pledge = forms.CharField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Order
        fields = ('total', 'comments', 'comments_other', 'avs', 'auth', 'payments')

    def clean(self):
        """Check for a value if designation is 'other'."""
        cd = self.cleaned_data
        error = None
        if cd.get('comments') == 'Other' and not cd.get('comments_other'):
            self.add_error(
                'comments_other',
                'Please provide a designation for your donation',
            )
        return cd


class GivingTuesdayDonationOrderForm(DonationOrderForm):
    """Donation form for giving tuesday campaign."""

    statement = forms.CharField(label="In honor of", required=False)
    comments = forms.CharField(
        label='Reason for honoring',
        widget=forms.Textarea,
        required=False,
    )
    binary = forms.ChoiceField(
        label='Can we share your story on social media?',
        required=False,
        initial='Yes',
        choices=BINARY_CHOICES, widget=forms.RadioSelect(),
    )

    class Meta:
        model = Order
        fields = ('total', 'statement', 'comments', 'binary', 'avs', 'auth', 'payments')


class PledgeContactForm(DonationContactForm):
    """
    Pledge Contact form, inherits everything from DonationContactForm and
    is merely a placeholder for view logic
    """
    pass


class GivingDayPledgeContactForm(DonationContactForm):
    """Same as above, but for Giving Day."""
    pass


class PledgeOrderForm(OrderForm):
    """A subscrition form for recurring billing."""

    total=forms.CharField(
        label='Gift installments',
        help_text='How much would you like to give for each installment.',
    )
    comments = forms.CharField(
        label = "Designation",
        help_text = '''
            Please indicate if you would like your gift to be directed to
            a specific area.
        ''',
        required=False,
    )
    payments = forms.IntegerField(
        widget=forms.Select(choices=PAYMENT),
        max_value=60,
        min_value=12,
        label="Duration",
        help_text='''
            Choose the number of years during which you want to donate
            the set amount above.
        ''',
    )
    cycle = forms.CharField(
        widget=forms.Select(choices=CYCLES),
        required=True,
        label="Frequency",
        help_text='''
            Choose how often the donation should be sent during the term
            of the pledge.
        ''',
    )

    class Meta:
        model = Order
        fields = ('total', 'cycle', 'payments', 'comments', 'avs', 'auth')


class ManagerContactForm(DonationContactForm):
    """Create a donation contact manually for things like cash donations."""

    first_name = forms.CharField(required=False)
    email = forms.EmailField(
        label='Your email address',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(ManagerContactForm, self).__init__(*args, **kwargs)
        self.fields.pop('state')
        self.fields.pop('postal_code')
        self.fields.pop('phone')
        self.fields.pop('city')
        self.fields.pop('address1')
        self.fields.pop('opt_in')
        self.fields.pop('matching_company')

    class Meta:
        model = DonationContact
        fields = ('first_name', 'last_name', 'relation', 'class_of', 'email')


class ManagerOrderForm(forms.ModelForm):
    """Create a donation order manually for things like cash donations."""

    promotion = forms.ModelChoiceField(
        queryset=Promotion.objects.all().order_by('-date_created'),
        required=False,
    )

    class Meta:
        model = Order
        fields = ('total', 'promotion')
