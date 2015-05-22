from django.contrib import admin
from djforms.security.models import ParkingTicketAppeal

class ParkingTicketAppealAdmin(admin.ModelAdmin):
    model = ParkingTicketAppeal
    list_display  = (
        'last_name','first_name','college_id','email','created_at'
    )
    search_fields = (
        'last_name','first_name','college_id','email'
    )
    ordering = ['-created_at',]
    readonly_fields = ('created_at',)

admin.site.register(ParkingTicketAppeal, ParkingTicketAppealAdmin)
