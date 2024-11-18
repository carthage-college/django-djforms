# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from djforms.core.models import GenericContact
from djtools.fields.helpers import upload_to_path
from image_cropping import ImageRatioField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


IMG_EXTENSIONS = [FileExtensionValidator(allowed_extensions=['jpg']),]


class Contact(GenericContact):
    """Data model for contact form."""
    second_name = models.CharField(
        "Middle name",
        max_length=128,
        null=True,
        blank=True,
    )
    previous_name = models.CharField(
        "Previous name",
        max_length=128,
        help_text="e.g. Maiden name",
        null=True,
        blank=True,
    )
    salutation = models.CharField(
        max_length=16,
        help_text="e.g. Ms., Mr. Dr.",
        null=True,
        blank=True,
    )
    suffix = models.CharField(
        max_length=16,
        help_text="e.g. PhD., Esquire, Jr., Sr., III",
        null=True,
        blank=True,
    )
    # core
    classyear = models.CharField(
        "Class",
        max_length=4,
        null=True,
        blank=True,
    )
    spousename = models.CharField(
        "Spouse's name",
        max_length=128,
        null=True,
        blank=True,
    )
    spousepreviousname = models.CharField(
        "Spouse's previous name",
        max_length=32,
        null=True,
        blank=True,
        help_text="e.g. maiden name",
    )
    spouseyear = models.CharField(
        "Spouse's class",
        max_length=4,
        null=True,
        blank=True,
    )
    hometown = models.CharField(max_length=128)
    classnote = models.TextField("Note")
    alumnistatus = models.BooleanField(
        "Almuni office status",
        default=False,
        help_text="Approved by Alumni Office",
    )
    alumnicomments = models.TextField(
        "Alumni office comments",
        null=True,
        blank=True,
    )
    pubstatus = models.BooleanField(
        "Publication status",
        default=False,
        help_text="Approved for publication on web and in Carthaginian",
    )
    pubstatusdate = models.DateTimeField(
        "Web Publication Date",
        null=True,
        blank=True,
    )
    carthaginianstatus = models.BooleanField(
        "Carthiginian status",
        default=False,
        help_text="Published in the Carthaginian",
    )
    category = models.CharField("Category", max_length=32)
    picture = models.ImageField(
        "Photo",
        max_length=255,
        upload_to=upload_to_path,
        validators=IMG_EXTENSIONS,
        help_text="75 dpi and .jpg only",
        null=True,
        blank=True,
    )
    # size is "width x height"
    cropping = ImageRatioField('picture', '800x600', allow_fullsize=True, free_crop=True)
    thumbnail = ImageSpecField(
        source='picture',
        processors=[ResizeToFill(200, 170)],
        format='JPEG',
        options={'quality': 80},
    )
    caption = models.CharField(
        "Caption for the photo",
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'alumni_classnotes_contact'
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __str__(self):
        return "{0}, {1} ({2})".format(
            self.last_name, self.first_name, self.classyear,
        )

    def get_edit_url(self):
        """Return the URL to edit the object on the admin."""
        return reverse("admin:classnotes_contact_change", args=[self.id])


    def get_slug(self):
        """Required for the upload_to_path() function."""
        return 'files/alumni/classnotes/photos'

    def admin_image(self):
        if self.picture:
            return mark_safe('<a href="{}{}">Photo</a>'.format(
                settings.MEDIA_URL, self.picture,
            ))
        else:
            return None
    admin_image.allow_tags = True
