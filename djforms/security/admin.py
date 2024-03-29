# -*- coding: utf-8 -*-

from django.contrib import admin
from djforms.security.models import ParkingTicketAppeal


class ParkingTicketAppealAdmin(admin.ModelAdmin):
    model = ParkingTicketAppeal
    list_display  = (
        'last_name',
        'first_name',
        'cid',
        'email',
        'created_at',
        'residency_status',
        'vehicle_make',
        'vehicle_model',
        'license_plate',
        'state',
        'permit_type',
        'permit_number',
        'citation_number',
        'citation_date',
        'towed',
    )


admin.site.register(ParkingTicketAppeal, ParkingTicketAppealAdmin)
