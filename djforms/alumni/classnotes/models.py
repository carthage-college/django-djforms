from django.db import models
from django.conf import settings
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from djforms.core.models import GenericContact

from djtools.fields.helpers import upload_to_path


class Contact(GenericContact):
    """
    Model Contact
    """
    second_name = models.CharField(
        "Middle name",
        max_length=128, null=True, blank=True
    )
    previous_name = models.CharField(
        "Previous name",
        max_length=128, null=True, blank=True,
        help_text="e.g. Maiden name",
    )
    salutation = models.CharField(
        max_length=16, null=True, blank=True,
        help_text="e.g. Ms., Mr. Dr.",
    )
    suffix = models.CharField(
        max_length=16, null=True, blank=True,
        help_text="e.g. PhD., Esquire, Jr., Sr., III",
    )
    # core
    classyear = models.CharField(
        "Class",
        max_length=4, null=True, blank=True
    )
    spousename = models.CharField(
        "Spouse's name",
        max_length=128, blank=True, null=True
    )
    spousepreviousname = models.CharField(
        "Spouse's previous name",
        max_length=32, blank=True, null=True,
        help_text="e.g. maiden name",
    )
    spouseyear = models.CharField(
        "Spouse's class",
        max_length=4, blank=True, null=True
    )
    hometown = models.CharField(max_length=128)
    classnote = models.TextField("Note")
    alumnistatus = models.BooleanField(
        "Almuni office status",
        default=False,
        help_text="Approved by Alumni Office"
    )
    alumnicomments = models.TextField(
        "Alumni office comments",
        blank=True, null=True
    )
    pubstatus = models.BooleanField(
        "Publication status",
        default=False,
        help_text="Approved for publication on web and in Carthaginian"
    )
    pubstatusdate = models.DateTimeField(
        "Web Publication Date",
        blank=True, null=True
    )
    carthaginianstatus = models.BooleanField(
        "Carthiginian status",
        default=False,
        help_text="Published in the Carthaginian"
    )
    category = models.CharField(
        "Category", max_length=32
    )
    picture = models.ImageField(
        "Photo",
        max_length=255, blank=True, null=True,
        upload_to=upload_to_path,
        help_text="75 dpi and .jpg only",
    )
    thumbnail = ImageSpecField(
        source='picture',
        processors=[ResizeToFill(200, 170)],
        format='JPEG',
        options={'quality': 80}
    )
    caption = models.CharField(
        "Caption for the photo",
        max_length=255, blank=True, null=True
    )

    class Meta:
        db_table = 'alumni_classnotes_contact'
        ordering  = ['-created_at']
        get_latest_by = 'created_at'

    def __unicode__(self):
        return "{}, {} ({})".format(
            self.last_name, self.first_name, self.classyear
        )

    def get_edit_url(self):
        """
        return "http://{}/forms/admin/classnotes/contact/{}/".format(
            settings.SERVER_URL, self.id
        )
        """
        return reverse("admin:classnotes_contact_change", args=[self.id])


    def get_slug(self):
        return "files/alumni/classnotes/photos"

    def admin_image(self):
        if self.picture:
            return '<a href="{}{}">Photo</a>'.format(
                settings.MEDIA_URL,self.picture
            )
        else:
            return None
    admin_image.allow_tags = True
