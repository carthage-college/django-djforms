from django.db import models
from django.db.models import Q
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from localflavor.us.models import USStateField
from taggit.managers import TaggableManager

from djtools.fields.helpers import upload_to_path
from djtools.fields.validators import MimetypeValidator

import datetime

BINARY_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)
GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Decline to state','Decline to state'),
)
MARITAL_CHOICES = (
    ('Single','Single'),
    ('Married','Married'),
    ('Separated','Separated'),
    ('Divorced','Divorced'),
    ('Widowed','Widowed')
)
SEMESTER_CHOICES = (
    ('Fall', 'Fall'),
    ('January', 'January'),
    ('Spring', 'Spring'),
    ('Summer', 'Summer'),
)
YEAR_CHOICES = (
    ('','---------'),
    ('1','Freshman'),
    ('2','Sophmore'),
    ('3','Junior'),
    ('4','Senior'),
    ('5','Graduate')
)
PAYMENT_CHOICES = (
    ('Credit Card', 'Credit Card'),
    ('Check', 'Check'),
    ('Cash/Money Order', 'Cash/Money Order'),
)
SHIRT_SIZES = (
    ('','---------'),
    ("XS",  "Extra Small"),
    ("S",   "Small"),
    ("M",   "Medium"),
    ("L",   "Large"),
    ("XL",  "Extra Large"),
    ("2X",  "2X Large"),
    ("3X",  "3X Large")
)

SALUTATION_TITLES = (
    ('','-------'),
    ("Mrs.","Mrs."),
    ("Ms.","Ms."),
    ("Mr.","Mr."),
    ("Master.","Master."),
    ("Prof.","Prof."),
    ("Dr.","Dr."),
)
if settings.DEBUG:
    REQ = {'class': 'required'}
else:
    REQ = {'class': 'required','required': 'required'}

try:
    YEARS1 = [(x, x) for x in reversed(range(1926,datetime.date.today().year +1))]
    YEARS3 = [(x, x) for x in reversed(range(1926,datetime.date.today().year +3))]
except:
    YEARS1 = [(x, x) for x in reversed(xrange(1926,datetime.date.today().year +1))]
    YEARS3 = [(x, x) for x in reversed(xrange(1926,datetime.date.today().year +3))]


class GenericChoice(models.Model):
    """For making choices for select fields in forms."""

    name = models.CharField(unique=True, max_length=255)
    value = models.CharField(max_length=255)
    ranking = models.IntegerField(
        verbose_name="Ranking",
        null=True, blank=True, default=0,
        help_text="""
          A number from 0 to 999 to determine this object's position in a list.
        """
    )
    active = models.BooleanField(
        help_text="""
            Do you want the field to be visable on your form?
        """,
        verbose_name='Is active?', default=True
    )
    tags = TaggableManager()

    def __unicode__(self):
        return self.name

    def tag_list(self):
        return u", ".join(o.name for o in self.tags.all())

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
        return u'{0}, {1}'.format(self.last_name, self.first_name)


class UserProfile(models.Model):
    """User profile model."""

    user = models.OneToOneField(
        User, related_name='userprofile', unique=True,
        on_delete=models.CASCADE
    )
    creation_date = models.DateTimeField(default=datetime.datetime.now)
    country = models.CharField(max_length=2, null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(
        max_length=12, verbose_name="Phone Number",
        help_text="Format: XXX-XXX-XXXX", null=True, blank=True
    )
    address = models.CharField(
        max_length=255, verbose_name = "Address", null=True, blank=True
    )
    city = models.CharField(
        max_length=128, verbose_name = "City", null=True, blank=True
    )
    state = USStateField(
        null=True, blank=True,
        default='WI'
    )
    zip = models.CharField(
        max_length=10, verbose_name = "Zip code", null=True, blank=True
    )
    dob = models.DateField(
        "Birthday", null=True, blank=True
    )
    gender = models.CharField(
        max_length=16, choices=GENDER_CHOICES, null=True, blank=True
    )
    campus_address = models.CharField(
        "Campus Address", max_length=64, null=True, blank=True
    )
    campus_box = models.CharField(
        "Campus Box #", max_length=4, null=True, blank=True
    )
    college_id = models.CharField(
        "Carthage ID", max_length=7,null=True, blank=True
    )
    college_year = models.CharField(
        "Current Year at Carthage", max_length=1,
        choices=YEAR_CHOICES, null=True, blank=True
    )

    def __unicode__(self):
        return "{} {}'s profile with username: {}".format(
            self.user.first_name, self.user.last_name, self.user.username
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
        upload_to=upload_to_path, max_length=255,
        validators=[MimetypeValidator('image/jpeg')],
    )
    thumbnail = ImageSpecField(
        source='original',
        processors=[ResizeToFill(100, 134)],
        format='JPEG',
        options={'quality': 80}
    )
    caption = models.TextField(
        'Caption', null=True, blank=True
    )

    def get_slug(self):
        return "photos/"


class Department(models.Model):
    """Departmenti."""

    name = models.CharField(
        max_length=100, verbose_name = "Department Name"
    )
    slug = models.SlugField(unique=True)
    number = models.CharField(
        max_length=3, verbose_name = "Department Number"
    )
    contact_name = models.CharField(
        max_length=100, verbose_name = "Department Contact"
    )
    contact_phone = models.CharField(
        max_length=100, verbose_name = "Department Phone"
    )
    tags = TaggableManager()

    class Meta:
        verbose_name_plural = "Departments"
        db_table = 'core_departments'
        ordering = ('name',)

    class Admin:
        prepopulated_fields = {'slug': ('name',)}

    def __unicode__(self):
        return '{} '.format(self.name)

    def get_absolute_url(self):
        return ('department_detail', None, { 'slug':self.slug })


class Promotion(models.Model):
    """Promotions and campaigns for ecommerce apps."""

    user = models.ForeignKey(
        User, verbose_name="Created by",
        related_name="matching_campaign_user",
        editable=False, null=True, blank=True, on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    title = models.CharField(max_length=255)
    designation = models.CharField(
        max_length=255, null=True, blank=True
    )
    slug = models.SlugField(
        max_length=255, unique=True
    )
    description = models.TextField(
        help_text="This information will appear above the form.",
        null=True, blank=True
    )
    about = models.TextField(
        help_text = """
            This information will appear in the sidebar next to the form.
        """, editable=False, null=True, blank=True
    )
    thank_you = models.TextField(
        help_text = """
            This information will be appear after the visitor
            successfully submits the form.
        """,
        null=True, blank=True
    )
    email_info = models.TextField(
        "Email content",
        help_text = """
            This information will be sent to the contact email address
            of the person filling out the form.
        """,
        null=True, blank=True
    )
    amount = models.DecimalField(
        decimal_places=2, max_digits=10,
        null = True, blank = True
    )
    donors = models.IntegerField(
        null=True, blank=True
    )
    institutional = models.BooleanField(
        default=False, editable=False
    )
    '''
    ratio = models.CharField(
        max_length=8,
        null=True, blank=True
    )
    '''

    def __unicode__(self):
        return self.title

    def all(self):
        objs = self.order_set.filter(Q(status="approved") | Q(status="manual"))
        return objs

    def count(self):
        return self.order_set.count()

    def amount_total(self):
        total = 0
        for obj in self.all():
            total += obj.total
        '''
        if self.ratio:
            r = self.ratio.split(':')
            total = int(r[0] * total) + int(r[1] * total)
        '''
        return total

    def percent(self):
        if self.donors:
            p = round(float(self.count())/float(self.donors) * 100,2)
        elif self.amount:
            p = round(int((self.amount_total() / self.amount) * 100),2)
        else:
            p = None
        return p

    def total(self):
        if self.donors:
            count = self.count()
        else:
            count = self.amount_total()
        return count


STATE_CHOICES = (
    ('','State'),
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
    ('AF', _(u'Afghanistan')),
    ('AX', _(u'\xc5land Islands')),
    ('AL', _(u'Albania')),
    ('DZ', _(u'Algeria')),
    ('AS', _(u'American Samoa')),
    ('AD', _(u'Andorra')),
    ('AO', _(u'Angola')),
    ('AI', _(u'Anguilla')),
    ('AQ', _(u'Antarctica')),
    ('AG', _(u'Antigua and Barbuda')),
    ('AR', _(u'Argentina')),
    ('AM', _(u'Armenia')),
    ('AW', _(u'Aruba')),
    ('AU', _(u'Australia')),
    ('AT', _(u'Austria')),
    ('AZ', _(u'Azerbaijan')),
    ('BS', _(u'Bahamas')),
    ('BH', _(u'Bahrain')),
    ('BD', _(u'Bangladesh')),
    ('BB', _(u'Barbados')),
    ('BY', _(u'Belarus')),
    ('BE', _(u'Belgium')),
    ('BZ', _(u'Belize')),
    ('BJ', _(u'Benin')),
    ('BM', _(u'Bermuda')),
    ('BT', _(u'Bhutan')),
    ('BO', _(u'Bolivia, Plurinational State of')),
    ('BQ', _(u'Bonaire, Sint Eustatius and Saba')),
    ('BA', _(u'Bosnia and Herzegovina')),
    ('BW', _(u'Botswana')),
    ('BV', _(u'Bouvet Island')),
    ('BR', _(u'Brazil')),
    ('IO', _(u'British Indian Ocean Territory')),
    ('BN', _(u'Brunei Darussalam')),
    ('BG', _(u'Bulgaria')),
    ('BF', _(u'Burkina Faso')),
    ('BI', _(u'Burundi')),
    ('KH', _(u'Cambodia')),
    ('CM', _(u'Cameroon')),
    ('CA', _(u'Canada')),
    ('CV', _(u'Cape Verde')),
    ('KY', _(u'Cayman Islands')),
    ('CF', _(u'Central African Republic')),
    ('TD', _(u'Chad')),
    ('CL', _(u'Chile')),
    ('CN', _(u'China')),
    ('CX', _(u'Christmas Island')),
    ('CC', _(u'Cocos (Keeling) Islands')),
    ('CO', _(u'Colombia')),
    ('KM', _(u'Comoros')),
    ('CG', _(u'Congo')),
    ('CD', _(u'Congo, The Democratic Republic of the')),
    ('CK', _(u'Cook Islands')),
    ('CR', _(u'Costa Rica')),
    ('CI', _(u"C\xf4te D'ivoire")),
    ('HR', _(u'Croatia')),
    ('CU', _(u'Cuba')),
    ('CW', _(u'Cura\xe7ao')),
    ('CY', _(u'Cyprus')),
    ('CZ', _(u'Czech Republic')),
    ('DK', _(u'Denmark')),
    ('DJ', _(u'Djibouti')),
    ('DM', _(u'Dominica')),
    ('DO', _(u'Dominican Republic')),
    ('EC', _(u'Ecuador')),
    ('EG', _(u'Egypt')),
    ('SV', _(u'El Salvador')),
    ('GQ', _(u'Equatorial Guinea')),
    ('ER', _(u'Eritrea')),
    ('EE', _(u'Estonia')),
    ('ET', _(u'Ethiopia')),
    ('FK', _(u'Falkland Islands (Malvinas)')),
    ('FO', _(u'Faroe Islands')),
    ('FJ', _(u'Fiji')),
    ('FI', _(u'Finland')),
    ('FR', _(u'France')),
    ('GF', _(u'French Guiana')),
    ('PF', _(u'French Polynesia')),
    ('TF', _(u'French Southern Territories')),
    ('GA', _(u'Gabon')),
    ('GM', _(u'Gambia')),
    ('GE', _(u'Georgia')),
    ('DE', _(u'Germany')),
    ('GH', _(u'Ghana')),
    ('GI', _(u'Gibraltar')),
    ('GR', _(u'Greece')),
    ('GL', _(u'Greenland')),
    ('GD', _(u'Grenada')),
    ('GP', _(u'Guadeloupe')),
    ('GU', _(u'Guam')),
    ('GT', _(u'Guatemala')),
    ('GG', _(u'Guernsey')),
    ('GN', _(u'Guinea')),
    ('GW', _(u'Guinea-bissau')),
    ('GY', _(u'Guyana')),
    ('HT', _(u'Haiti')),
    ('HM', _(u'Heard Island and McDonald Islands')),
    ('VA', _(u'Holy See (Vatican City State)')),
    ('HN', _(u'Honduras')),
    ('HK', _(u'Hong Kong')),
    ('HU', _(u'Hungary')),
    ('IS', _(u'Iceland')),
    ('IN', _(u'India')),
    ('ID', _(u'Indonesia')),
    ('IR', _(u'Iran, Islamic Republic of')),
    ('IQ', _(u'Iraq')),
    ('IE', _(u'Ireland')),
    ('IM', _(u'Isle of Man')),
    ('IL', _(u'Israel')),
    ('IT', _(u'Italy')),
    ('JM', _(u'Jamaica')),
    ('JP', _(u'Japan')),
    ('JE', _(u'Jersey')),
    ('JO', _(u'Jordan')),
    ('KZ', _(u'Kazakhstan')),
    ('KE', _(u'Kenya')),
    ('KI', _(u'Kiribati')),
    ('KP', _(u"Korea, Democratic People's Republic of")),
    ('KR', _(u'Korea, Republic of')),
    ('KW', _(u'Kuwait')),
    ('KG', _(u'Kyrgyzstan')),
    ('LA', _(u"Lao People's Democratic Republic")),
    ('LV', _(u'Latvia')),
    ('LB', _(u'Lebanon')),
    ('LS', _(u'Lesotho')),
    ('LR', _(u'Liberia')),
    ('LY', _(u'Libya')),
    ('LI', _(u'Liechtenstein')),
    ('LT', _(u'Lithuania')),
    ('LU', _(u'Luxembourg')),
    ('MO', _(u'Macao')),
    ('MK', _(u'Macedonia, The Former Yugoslav Republic of')),
    ('MG', _(u'Madagascar')),
    ('MW', _(u'Malawi')),
    ('MY', _(u'Malaysia')),
    ('MV', _(u'Maldives')),
    ('ML', _(u'Mali')),
    ('MT', _(u'Malta')),
    ('MH', _(u'Marshall Islands')),
    ('MQ', _(u'Martinique')),
    ('MR', _(u'Mauritania')),
    ('MU', _(u'Mauritius')),
    ('YT', _(u'Mayotte')),
    ('MX', _(u'Mexico')),
    ('FM', _(u'Micronesia, Federated States of')),
    ('MD', _(u'Moldova, Republic of')),
    ('MC', _(u'Monaco')),
    ('MN', _(u'Mongolia')),
    ('ME', _(u'Montenegro')),
    ('MS', _(u'Montserrat')),
    ('MA', _(u'Morocco')),
    ('MZ', _(u'Mozambique')),
    ('MM', _(u'Myanmar')),
    ('NA', _(u'Namibia')),
    ('NR', _(u'Nauru')),
    ('NP', _(u'Nepal')),
    ('NL', _(u'Netherlands')),
    ('NC', _(u'New Caledonia')),
    ('NZ', _(u'New Zealand')),
    ('NI', _(u'Nicaragua')),
    ('NE', _(u'Niger')),
    ('NG', _(u'Nigeria')),
    ('NU', _(u'Niue')),
    ('NF', _(u'Norfolk Island')),
    ('MP', _(u'Northern Mariana Islands')),
    ('NO', _(u'Norway')),
    ('OM', _(u'Oman')),
    ('PK', _(u'Pakistan')),
    ('PW', _(u'Palau')),
    ('PS', _(u'Palestinian Territory, Occupied')),
    ('PA', _(u'Panama')),
    ('PG', _(u'Papua New Guinea')),
    ('PY', _(u'Paraguay')),
    ('PE', _(u'Peru')),
    ('PH', _(u'Philippines')),
    ('PN', _(u'Pitcairn')),
    ('PL', _(u'Poland')),
    ('PT', _(u'Portugal')),
    ('PR', _(u'Puerto Rico')),
    ('QA', _(u'Qatar')),
    ('RE', _(u'R\xe9union')),
    ('RO', _(u'Romania')),
    ('RU', _(u'Russian Federation')),
    ('RW', _(u'Rwanda')),
    ('BL', _(u'Saint Barth\xe9lemy')),
    ('SH', _(u'Saint Helena, Ascension and Tristan Da Cunha')),
    ('KN', _(u'Saint Kitts and Nevis')),
    ('LC', _(u'Saint Lucia')),
    ('MF', _(u'Saint Martin (French Part)')),
    ('PM', _(u'Saint Pierre and Miquelon')),
    ('VC', _(u'Saint Vincent and the Grenadines')),
    ('WS', _(u'Samoa')),
    ('SM', _(u'San Marino')),
    ('ST', _(u'Sao Tome and Principe')),
    ('SA', _(u'Saudi Arabia')),
    ('SN', _(u'Senegal')),
    ('RS', _(u'Serbia')),
    ('SC', _(u'Seychelles')),
    ('SL', _(u'Sierra Leone')),
    ('SG', _(u'Singapore')),
    ('SX', _(u'Sint Maarten (Dutch Part)')),
    ('SK', _(u'Slovakia')),
    ('SI', _(u'Slovenia')),
    ('SB', _(u'Solomon Islands')),
    ('SO', _(u'Somalia')),
    ('ZA', _(u'South Africa')),
    ('GS', _(u'South Georgia and the South Sandwich Islands')),
    ('SS', _(u'South Sudan')),
    ('ES', _(u'Spain')),
    ('LK', _(u'Sri Lanka')),
    ('SD', _(u'Sudan')),
    ('SR', _(u'Suriname')),
    ('SJ', _(u'Svalbard and Jan Mayen')),
    ('SZ', _(u'Swaziland')),
    ('SE', _(u'Sweden')),
    ('CH', _(u'Switzerland')),
    ('SY', _(u'Syrian Arab Republic')),
    ('TW', _(u'Taiwan, Province of China')),
    ('TJ', _(u'Tajikistan')),
    ('TZ', _(u'Tanzania, United Republic of')),
    ('TH', _(u'Thailand')),
    ('TL', _(u'Timor-leste')),
    ('TG', _(u'Togo')),
    ('TK', _(u'Tokelau')),
    ('TO', _(u'Tonga')),
    ('TT', _(u'Trinidad and Tobago')),
    ('TN', _(u'Tunisia')),
    ('TR', _(u'Turkey')),
    ('TM', _(u'Turkmenistan')),
    ('TC', _(u'Turks and Caicos Islands')),
    ('TV', _(u'Tuvalu')),
    ('UG', _(u'Uganda')),
    ('UA', _(u'Ukraine')),
    ('AE', _(u'United Arab Emirates')),
    ('GB', _(u'United Kingdom')),
    ('US', _(u'United States')),
    ('UM', _(u'United States Minor Outlying Islands')),
    ('UY', _(u'Uruguay')),
    ('UZ', _(u'Uzbekistan')),
    ('VU', _(u'Vanuatu')),
    ('VE', _(u'Venezuela, Bolivarian Republic of')),
    ('VN', _(u'Viet Nam')),
    ('VG', _(u'Virgin Islands, British')),
    ('VI', _(u'Virgin Islands, U.S.')),
    ('WF', _(u'Wallis and Futuna')),
    ('EH', _(u'Western Sahara')),
    ('YE', _(u'Yemen')),
    ('ZM', _(u'Zambia')),
    ('ZW', _(u'Zimbabwe')),
)
