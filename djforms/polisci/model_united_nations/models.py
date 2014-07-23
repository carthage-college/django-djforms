from django.db import models
from djforms.processors.models import Contact

def disengage_country(sender, instance, **kwargs):
    if instance.delegation_1:
        instance.delegation_1.status = False
        instance.delegation_1.save()
    if instance.delegation_2:
        instance.delegation_2.status = False
        instance.delegation_2.save()
    if instance.delegation_3:
        instance.delegation_3.status = False
        instance.delegation_3.save()
    if instance.delegation_4:
        instance.delegation_4.status = False
        instance.delegation_4.save()
    if instance.delegation_5:
        instance.delegation_5.status = False
        instance.delegation_5.save()

class Country(models.Model):
    name = models.CharField(
        "Country name",
        max_length=128
    )
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return self.name

class Attender(Contact):
    """
    Model United Nations attender contact
    """
    school_name = models.CharField(
        "School name",
        max_length=100
    )
    office = models.CharField(max_length=100)
    number_of_del = models.IntegerField(
        "Number of delegations",
        max_length=2
    )
    number_of_stu = models.CharField(
        "Number of students",
        max_length=3
    )
    delegation_1 = models.ForeignKey(
        Country,
        related_name="mun_delegation_1",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    delegation_2 = models.ForeignKey(
        Country,
        related_name="mun_delegation_2",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    delegation_3 = models.ForeignKey(
        Country,
        related_name="mun_delegation_3",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    delegation_4 = models.ForeignKey(
        Country,
        related_name="mun_delegation_4",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    delegation_5 = models.ForeignKey(
        Country,
        related_name="mun_delegation_5",
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    comments = models.TextField(
        "Questions/Comments",
        null=True, blank=True
    )

models.signals.post_save.connect(disengage_country, sender=Attender)
