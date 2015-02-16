# -*- coding: utf-8 -*-
from django.db import models

from djforms.core.models import GenericContact
from djtools.fields.helpers import upload_to_path


class Nomination(GenericContact):
    # candidate
    candidate_first_name = models.CharField(max_length=128)
    candidate_last_name = models.CharField(max_length=128)
    candidate_class_year = models.CharField(
        "Candidate class year (if applicable)", max_length=4,
        null=True, blank=True
    )
    reason = models.TextField(
        "Reason for nomination",
        help_text = """
            Please explain in detail why you are nominating
            this individual for an honorary degree.
        """
    )
    links = models.TextField(
        """
        Links to relevant articles, sites, and other supporting material
        """
    )
    cv = models.FileField(
        "CV or résumé",
        upload_to=upload_to_path,
        max_length=768,
    )
    # nominator (includes fn,sn,email from GenericContact)
    class_year = models.CharField(
        "Your class year (if applicable)", max_length=4,
        null=True, blank=True
    )

    def __unicode__(self):
        return u'{} {}'.format(self.candidate_last_name, self.candidate_first_name)

    def get_slug(self):
        return "president/honorary-degree/nomination/"

