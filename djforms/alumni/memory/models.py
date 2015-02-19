from django.db import models
from django.core.urlresolvers import reverse

from djforms.core.models import Photo, Promotion, GenericContact

from localflavor.us.models import USStateField

class Questionnaire(GenericContact):
    second_name = models.CharField(
        max_length=30,
        null=True, blank=True
    )
    address1 = models.CharField(
        "Address",
        max_length=255
    )
    address2 = models.CharField(
        "",
        max_length=255
    )
    city = models.CharField(
        max_length=128
    )
    state = USStateField()
    postal_code = models.CharField(
        "Zip code",
        max_length=10
    )
    phone = models.CharField(
        "Phone number",
        max_length=18,
        help_text="Format: XXX-XXX-XXXX"
    )
    occupation1 = models.CharField(
        "Occupation",
        max_length=100,
        help_text = "What someone pays you to do.",
        null=True, blank=True
    )
    occupation2 = models.CharField(
        "Occupation",
        max_length=100,
        help_text = "What no one pays you to do but you do anyway.",
        null=True, blank=True
    )
    greek_parent = models.CharField(
        max_length=255,
        null=True, blank=True
    )
    greek_siblings = models.TextField(
        null=True, blank=True
    )
    why_carthage = models.TextField(
        "How did you choose to attend Carthage?",
        null=True, blank=True
    )
    professor = models.CharField(
        max_length=100,
        verbose_name = "Who was your favorite Carthage professor?",
        null=True, blank=True
    )
    professor_why = models.TextField(
        "Why?",
        null=True, blank=True
    )
    special = models.TextField(
        "What makes your class special?",
        null=True, blank=True
    )
    relive = models.TextField(
        verbose_name = """
            If you had the chance to relive a single Carthage moment
            or event, which one would you choose?
        """,
        null=True, blank=True
    )
    message = models.TextField(
        "Personal message for the Memory Book",
        help_text = """
            You may want to include family, hobbies, travel
            experiences and fond rememberances.
        """,
        null=True, blank=True
    )
    photos = models.ManyToManyField(
        Photo, verbose_name = "Photos",
        related_name = "alumni_memory_questionaire_photos",
        null=True, blank=True
    )
    promotion = models.ForeignKey(
        Promotion, null=True, blank=True
    )

    class Meta:
        db_table = "alumni_memory_questionnaire"

    def get_absolute_url(self):
        return reverse("memory_questionnaire_detail", args=[self.pk])

    def get_slug(self):
        return "president/honorary-degree/nomination/"
