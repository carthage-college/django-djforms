# -*- coding: utf-8 -*-

import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from djtools.fields.helpers import upload_to_path
from djtools.fields.validators import MimetypeValidator

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from localflavor.us.models import USStateField
from taggit.managers import TaggableManager


BINARY_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)
GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Decline to state', 'Decline to state'),
)
MARITAL_CHOICES = (
    ('Single', 'Single'),
    ('Married', 'Married'),
    ('Separated', 'Separated'),
    ('Divorced', 'Divorced'),
    ('Widowed', 'Widowed'),
)
SEMESTER_CHOICES = (
    ('Fall', 'Fall'),
    ('January', 'January'),
    ('Spring', 'Spring'),
    ('Summer', 'Summer'),
)
YEAR_CHOICES = (
    ('', '---------'),
    ('1', 'Freshman'),
    ('2', 'Sophmore'),
    ('3', 'Junior'),
    ('4', 'Senior'),
    ('5', 'Graduate'),
)
PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Check', 'Check'),
    ('Cash/Money Order', 'Cash/Money Order'),
)
SHIRT_SIZES = (
    ('','---------'),
    ('XS',  'Extra Small'),
    ('S',   'Small'),
    ('M',   'Medium'),
    ('L',   'Large'),
    ('XL',  'Extra Large'),
    ('2X',  '2X Large'),
    ('3X',  '3X Large'),
)
SALUTATION_TITLES = (
    ('', '-------'),
    ('Mrs.', 'Mrs.'),
    ('Ms.', 'Ms.'),
    ('Mr.', 'Mr.'),
    ('Master', 'Master'),
    ('Prof.', 'Prof.'),
    ('Dr.', 'Dr.'),
)
if settings.DEBUG:
    REQ = {'class': 'required'}
else:
    REQ = {'class': 'required','required': 'required'}

YEARS1 = [(x, x) for x in reversed(range(1926,datetime.date.today().year +1))]
YEARS3 = [(x, x) for x in reversed(range(1926,datetime.date.today().year +3))]


class GenericChoice(models.Model):
    """For making choices for select fields in forms."""

    name = models.CharField(unique=True, max_length=255)
    value = models.CharField(max_length=255)
    ranking = models.IntegerField(
        default=0,
        null=True,
        blank=True,
        help_text='A number from 0 to 999 to rank the position in a list.',
    )
    active = models.BooleanField(
        help_text='Do you want the field to be visable on your form?',
        verbose_name='Is active?',
        default=True,
    )
    tags = TaggableManager()

    def __str__(self):
        return self.name

    def tag_list(self):
        return ', '.join(o.name for o in self.tags.all())

    class Meta:
        ordering = ['ranking']


class GenericContact(models.Model):
    """For making contacts for forms."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    email = models.EmailField()

    class Meta:
        abstract = True
        ordering = ['last_name']

    def __unicode__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)


class UserProfile(models.Model):
    """User profile model."""

    user = models.OneToOneField(
        User,
        related_name='userprofile',
        unique=True,
        on_delete=models.CASCADE,
    )
    creation_date = models.DateTimeField(default=datetime.datetime.now)
    country = models.CharField(max_length=2, null=True, blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(
        max_length=12,
        help_text='Format: XXX-XXX-XXXX',
        null=True,
        blank=True,
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=128)
    state = USStateField(null=True, blank=True, default='WI')
    zip = models.CharField('Zip code', max_length=10, null=True, blank=True)
    dob = models.DateField('Birthday', null=True, blank=True)
    gender = models.CharField(
        max_length=16, choices=GENDER_CHOICES, null=True, blank=True,
    )
    campus_address = models.CharField(max_length=64, null=True, blank=True)
    campus_box = models.CharField(max_length=4, null=True, blank=True)
    college_year = models.CharField(
        'Current Year at Carthage',
        max_length=1,
        choices=YEAR_CHOICES,
        null=True,
        blank=True,
    )

    def __str__(self):
        return "{0} {1}'s profile with username: {2}".format(
            self.user.first_name, self.user.last_name, self.user.username,
        )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except:
        UserProfile.objects.create(user=instance)


class Photo(models.Model):
    title = models.CharField(max_length=255)
    original = models.ImageField(
        upload_to=upload_to_path,
        max_length=255,
        validators=[MimetypeValidator('image/jpeg')],
    )
    thumbnail = ImageSpecField(
        source='original',
        processors=[ResizeToFill(100, 134)],
        format='JPEG',
        options={'quality': 80},
    )
    caption = models.TextField(null=True, blank=True)

    def get_slug(self):
        return 'photos/'


class Department(models.Model):
    """Departmenti."""

    name = models.CharField('Department Name', max_length=100)
    slug = models.SlugField(unique=True)
    number = models.CharField(max_length=3, verbose_name = 'Department Number')
    contact_name = models.CharField('Department Contact', max_length=100)
    contact_phone = models.CharField('Department Phone', max_length=100)
    tags = TaggableManager()

    class Meta:
        verbose_name_plural = 'Departments'
        db_table = 'core_departments'
        ordering = ('name',)

    class Admin:
        prepopulated_fields = {'slug': ('name',)}

    def __str__(self):
        return self.name


class Promotion(models.Model):
    """Promotions and campaigns for ecommerce apps."""

    user = models.ForeignKey(
        User,
        verbose_name='Created by',
        related_name='matching_campaign_user',
        on_delete=models.CASCADE,
        editable=False,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(
        help_text='This information will appear above the form.',
        null=True,
        blank=True,
    )
    about = models.TextField(
        help_text='This information will appear in the sidebar next to the form.',
        editable=False,
        null=True,
        blank=True,
    )
    thank_you = models.TextField(
        help_text = '''
            This information will be appear after the visitor
            successfully submits the form.
        ''',
        null=True,
        blank=True,
    )
    email_info = models.TextField(
        'Email content',
        help_text='''
            This information will be sent to the contact email address
            of the person filling out the form.
        ''',
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
    )
    donors = models.IntegerField(null=True, blank=True)
    institutional = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return self.title

    def all(self):
        return self.order_set.filter(Q(status='approved') | Q(status='manual'))

    def count(self):
        return self.order_set.count()

    def amount_total(self):
        total = 0
        for promo in self.all():
            total += promo.total
        return total

    def percent(self):
        if self.donors:
            pcent = round(float(self.count()) / float(self.donors) * 100, 2)
        elif self.amount:
            pcent = round(int((self.amount_total() / self.amount) * 100), 2)
        else:
            pcent = None
        return pcent

    def total(self):
        if self.donors:
            count = self.count()
        else:
            count = self.amount_total()
        return count


STATE_CHOICES = (
    ('', '---State---'),
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AS', 'American Samoa'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('DC', 'District of Columbia'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('GU', 'Guam'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('MP', 'Northern Mariana Islands'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('PR', 'Puerto Rico'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VI', 'Virgin Islands'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
    ('OT','Other'),
)

COUNTRIES = (
    ('','Country'),
    ('AF', _('Afghanistan')),
    ('AX', _('\xc5land Islands')),
    ('AL', _('Albania')),
    ('DZ', _('Algeria')),
    ('AS', _('American Samoa')),
    ('AD', _('Andorra')),
    ('AO', _('Angola')),
    ('AI', _('Anguilla')),
    ('AQ', _('Antarctica')),
    ('AG', _('Antigua and Barbuda')),
    ('AR', _('Argentina')),
    ('AM', _('Armenia')),
    ('AW', _('Aruba')),
    ('AU', _('Australia')),
    ('AT', _('Austria')),
    ('AZ', _('Azerbaijan')),
    ('BS', _('Bahamas')),
    ('BH', _('Bahrain')),
    ('BD', _('Bangladesh')),
    ('BB', _('Barbados')),
    ('BY', _('Belarus')),
    ('BE', _('Belgium')),
    ('BZ', _('Belize')),
    ('BJ', _('Benin')),
    ('BM', _('Bermuda')),
    ('BT', _('Bhutan')),
    ('BO', _('Bolivia, Plurinational State of')),
    ('BQ', _('Bonaire, Sint Eustatius and Saba')),
    ('BA', _('Bosnia and Herzegovina')),
    ('BW', _('Botswana')),
    ('BV', _('Bouvet Island')),
    ('BR', _('Brazil')),
    ('IO', _('British Indian Ocean Territory')),
    ('BN', _('Brunei Darussalam')),
    ('BG', _('Bulgaria')),
    ('BF', _('Burkina Faso')),
    ('BI', _('Burundi')),
    ('KH', _('Cambodia')),
    ('CM', _('Cameroon')),
    ('CA', _('Canada')),
    ('CV', _('Cape Verde')),
    ('KY', _('Cayman Islands')),
    ('CF', _('Central African Republic')),
    ('TD', _('Chad')),
    ('CL', _('Chile')),
    ('CN', _('China')),
    ('CX', _('Christmas Island')),
    ('CC', _('Cocos (Keeling) Islands')),
    ('CO', _('Colombia')),
    ('KM', _('Comoros')),
    ('CG', _('Congo')),
    ('CD', _('Congo, The Democratic Republic of the')),
    ('CK', _('Cook Islands')),
    ('CR', _('Costa Rica')),
    ('CI', _(u"C\xf4te D'ivoire")),
    ('HR', _('Croatia')),
    ('CU', _('Cuba')),
    ('CW', _('Cura\xe7ao')),
    ('CY', _('Cyprus')),
    ('CZ', _('Czech Republic')),
    ('DK', _('Denmark')),
    ('DJ', _('Djibouti')),
    ('DM', _('Dominica')),
    ('DO', _('Dominican Republic')),
    ('EC', _('Ecuador')),
    ('EG', _('Egypt')),
    ('SV', _('El Salvador')),
    ('GQ', _('Equatorial Guinea')),
    ('ER', _('Eritrea')),
    ('EE', _('Estonia')),
    ('ET', _('Ethiopia')),
    ('FK', _('Falkland Islands (Malvinas)')),
    ('FO', _('Faroe Islands')),
    ('FJ', _('Fiji')),
    ('FI', _('Finland')),
    ('FR', _('France')),
    ('GF', _('French Guiana')),
    ('PF', _('French Polynesia')),
    ('TF', _('French Southern Territories')),
    ('GA', _('Gabon')),
    ('GM', _('Gambia')),
    ('GE', _('Georgia')),
    ('DE', _('Germany')),
    ('GH', _('Ghana')),
    ('GI', _('Gibraltar')),
    ('GR', _('Greece')),
    ('GL', _('Greenland')),
    ('GD', _('Grenada')),
    ('GP', _('Guadeloupe')),
    ('GU', _('Guam')),
    ('GT', _('Guatemala')),
    ('GG', _('Guernsey')),
    ('GN', _('Guinea')),
    ('GW', _('Guinea-bissau')),
    ('GY', _('Guyana')),
    ('HT', _('Haiti')),
    ('HM', _('Heard Island and McDonald Islands')),
    ('VA', _('Holy See (Vatican City State)')),
    ('HN', _('Honduras')),
    ('HK', _('Hong Kong')),
    ('HU', _('Hungary')),
    ('IS', _('Iceland')),
    ('IN', _('India')),
    ('ID', _('Indonesia')),
    ('IR', _('Iran, Islamic Republic of')),
    ('IQ', _('Iraq')),
    ('IE', _('Ireland')),
    ('IM', _('Isle of Man')),
    ('IL', _('Israel')),
    ('IT', _('Italy')),
    ('JM', _('Jamaica')),
    ('JP', _('Japan')),
    ('JE', _('Jersey')),
    ('JO', _('Jordan')),
    ('KZ', _('Kazakhstan')),
    ('KE', _('Kenya')),
    ('KI', _('Kiribati')),
    ('KP', _(u"Korea, Democratic People's Republic of")),
    ('KR', _('Korea, Republic of')),
    ('KW', _('Kuwait')),
    ('KG', _('Kyrgyzstan')),
    ('LA', _(u"Lao People's Democratic Republic")),
    ('LV', _('Latvia')),
    ('LB', _('Lebanon')),
    ('LS', _('Lesotho')),
    ('LR', _('Liberia')),
    ('LY', _('Libya')),
    ('LI', _('Liechtenstein')),
    ('LT', _('Lithuania')),
    ('LU', _('Luxembourg')),
    ('MO', _('Macao')),
    ('MK', _('Macedonia, The Former Yugoslav Republic of')),
    ('MG', _('Madagascar')),
    ('MW', _('Malawi')),
    ('MY', _('Malaysia')),
    ('MV', _('Maldives')),
    ('ML', _('Mali')),
    ('MT', _('Malta')),
    ('MH', _('Marshall Islands')),
    ('MQ', _('Martinique')),
    ('MR', _('Mauritania')),
    ('MU', _('Mauritius')),
    ('YT', _('Mayotte')),
    ('MX', _('Mexico')),
    ('FM', _('Micronesia, Federated States of')),
    ('MD', _('Moldova, Republic of')),
    ('MC', _('Monaco')),
    ('MN', _('Mongolia')),
    ('ME', _('Montenegro')),
    ('MS', _('Montserrat')),
    ('MA', _('Morocco')),
    ('MZ', _('Mozambique')),
    ('MM', _('Myanmar')),
    ('NA', _('Namibia')),
    ('NR', _('Nauru')),
    ('NP', _('Nepal')),
    ('NL', _('Netherlands')),
    ('NC', _('New Caledonia')),
    ('NZ', _('New Zealand')),
    ('NI', _('Nicaragua')),
    ('NE', _('Niger')),
    ('NG', _('Nigeria')),
    ('NU', _('Niue')),
    ('NF', _('Norfolk Island')),
    ('MP', _('Northern Mariana Islands')),
    ('NO', _('Norway')),
    ('OM', _('Oman')),
    ('PK', _('Pakistan')),
    ('PW', _('Palau')),
    ('PS', _('Palestinian Territory, Occupied')),
    ('PA', _('Panama')),
    ('PG', _('Papua New Guinea')),
    ('PY', _('Paraguay')),
    ('PE', _('Peru')),
    ('PH', _('Philippines')),
    ('PN', _('Pitcairn')),
    ('PL', _('Poland')),
    ('PT', _('Portugal')),
    ('PR', _('Puerto Rico')),
    ('QA', _('Qatar')),
    ('RE', _('R\xe9union')),
    ('RO', _('Romania')),
    ('RU', _('Russian Federation')),
    ('RW', _('Rwanda')),
    ('BL', _('Saint Barth\xe9lemy')),
    ('SH', _('Saint Helena, Ascension and Tristan Da Cunha')),
    ('KN', _('Saint Kitts and Nevis')),
    ('LC', _('Saint Lucia')),
    ('MF', _('Saint Martin (French Part)')),
    ('PM', _('Saint Pierre and Miquelon')),
    ('VC', _('Saint Vincent and the Grenadines')),
    ('WS', _('Samoa')),
    ('SM', _('San Marino')),
    ('ST', _('Sao Tome and Principe')),
    ('SA', _('Saudi Arabia')),
    ('SN', _('Senegal')),
    ('RS', _('Serbia')),
    ('SC', _('Seychelles')),
    ('SL', _('Sierra Leone')),
    ('SG', _('Singapore')),
    ('SX', _('Sint Maarten (Dutch Part)')),
    ('SK', _('Slovakia')),
    ('SI', _('Slovenia')),
    ('SB', _('Solomon Islands')),
    ('SO', _('Somalia')),
    ('ZA', _('South Africa')),
    ('GS', _('South Georgia and the South Sandwich Islands')),
    ('SS', _('South Sudan')),
    ('ES', _('Spain')),
    ('LK', _('Sri Lanka')),
    ('SD', _('Sudan')),
    ('SR', _('Suriname')),
    ('SJ', _('Svalbard and Jan Mayen')),
    ('SZ', _('Swaziland')),
    ('SE', _('Sweden')),
    ('CH', _('Switzerland')),
    ('SY', _('Syrian Arab Republic')),
    ('TW', _('Taiwan, Province of China')),
    ('TJ', _('Tajikistan')),
    ('TZ', _('Tanzania, United Republic of')),
    ('TH', _('Thailand')),
    ('TL', _('Timor-leste')),
    ('TG', _('Togo')),
    ('TK', _('Tokelau')),
    ('TO', _('Tonga')),
    ('TT', _('Trinidad and Tobago')),
    ('TN', _('Tunisia')),
    ('TR', _('Turkey')),
    ('TM', _('Turkmenistan')),
    ('TC', _('Turks and Caicos Islands')),
    ('TV', _('Tuvalu')),
    ('UG', _('Uganda')),
    ('UA', _('Ukraine')),
    ('AE', _('United Arab Emirates')),
    ('GB', _('United Kingdom')),
    ('US', _('United States')),
    ('UM', _('United States Minor Outlying Islands')),
    ('UY', _('Uruguay')),
    ('UZ', _('Uzbekistan')),
    ('VU', _('Vanuatu')),
    ('VE', _('Venezuela, Bolivarian Republic of')),
    ('VN', _('Viet Nam')),
    ('VG', _('Virgin Islands, British')),
    ('VI', _('Virgin Islands, U.S.')),
    ('WF', _('Wallis and Futuna')),
    ('EH', _('Western Sahara')),
    ('YE', _('Yemen')),
    ('ZM', _('Zambia')),
    ('ZW', _('Zimbabwe')),
)
