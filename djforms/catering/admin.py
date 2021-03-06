from django.contrib import admin
from djforms.catering.models import Event

class EventAdmin(admin.ModelAdmin):
    model = Event
    ordering = ['-created_on','created_on','department']
    list_display  = (
        'event_name','created_on',
        'first_name','last_name','email','department'
    )
    search_fields = (
        'user__last_name','user__first_name','user__email','event_name'
    )
    raw_id_fields = ('user',)

admin.site.register(Event, EventAdmin)
