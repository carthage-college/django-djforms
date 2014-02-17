from django.db import models

from djforms.core.models import BINARY_CHOICES
from djforms.processors.models import Contact

from tagging import fields, managers

SECTOR_CHOICES = (
    ('','---------'),
    ('Publisher','Publisher'),
    ('Aggregator or distributor','Aggregator or distributor'),
    ('Open Source/Access','Open Source/Access'),
    ('Audio material','Audio material'),
    ('Internet content','Internet content'),
    ('Tools','Tools'),
)

class CourseFerenceAttender(Contact):

    affiliation         = models.CharField("Institution/Organization", max_length="256", null=True, blank=True)
    job_title           = models.CharField(max_length="128", null=True, blank=True)

    class Meta:
        db_table        = 'course_ference_attender'

class CourseFerenceVendor(CourseFerenceAttender):

    sector              = models.CharField("Organizational focus", max_length="32", choices=SECTOR_CHOICES)
    description         = models.TextField("Resources/Materials", help_text="Brief description of resources/materials you provide to libraries")
    swag                = models.CharField(max_length=3, choices=BINARY_CHOICES, help_text="Are you able to possibly offer special opportunities, prizes, freebies to attendees (such as drawings, product previews, codes for a free item, etc?)")
    discussion          = models.CharField(max_length=3, choices=BINARY_CHOICES, help_text="Are you able to participate in either an online discussion forum or live chat to further enhance interaction with attendees?")

    class Meta:
        db_table        = 'course_ference_vendor'

