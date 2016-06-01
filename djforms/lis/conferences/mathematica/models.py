from django.db import models

from djforms.processors.models import Contact


class Registration(Contact):

    affiliation = models.CharField(
        "Institution/Organization", max_length="256", null=True, blank=True
    )
    job_title = models.CharField(
        max_length="128", null=True, blank=True
    )
    group_members = models.TextField(
        "Group members", null=True, blank=True,
        help_text = """
            For those choosing the group discount,
            please include all group members' names,
            email addresses, and titles.
        """
    )

    class Meta:
        db_table = 'lis_mathematica_registration'
