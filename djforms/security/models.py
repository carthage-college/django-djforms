from django.db import models
from djforms.core.models import GenericContact, GenericChoice


class ParkingTicketAppeal(GenericContact):
    college_id = models.CharField(
        "Carthage ID#", max_length=10
    )
    residency_status = models.ForeignKey(
        GenericChoice,
        related_name='parking_ticket_appeal_residency_status',
        on_delete=models.CASCADE,
    )
    vehicle_make = models.CharField(
        "Vehicle Make", max_length=40
    )
    vehicle_model = models.CharField(
        "Vehicle Model", max_length=40
    )
    license_plate = models.CharField(
        "License Plate", max_length=20
    )
    state = models.CharField(
        "State", max_length=20
    )
    permit_type = models.ForeignKey(
        GenericChoice,
        related_name='parking_ticket_appeal_permit_type',
        on_delete=models.CASCADE,
    )
    permit_number = models.CharField(
        "Permit Number", max_length=30
    )
    citation_number = models.CharField(
        "Citation Number", max_length=30
    )
    citation_date = models.DateField(
        "Date of citation",
        auto_now=False
    )
    towed = models.CharField(
        "Was your vehicle Towed?",
        max_length=8
    )
    appeal_box = models.TextField(
        "Comments",
        help_text="Please provide your comments in support of your appeal."
    )
