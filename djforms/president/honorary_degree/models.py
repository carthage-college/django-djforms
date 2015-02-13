# -*- coding: utf-8 -*-
from django.db import models

from djforms.core.models import GenericContact

from uuid import uuid4

from os.path import join

def upload_to_path(self, filename):
    """
    Rename file to random string and generate path for a file field.
    """
    ext = filename.split('.')[-1]
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)
    path = "files/{}".format(
        self.get_slug()
    )
    return join(path, filename)


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

