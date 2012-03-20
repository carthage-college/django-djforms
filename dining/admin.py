from django.contrib import admin
from djforms.dining.models import Event

class EventAdmin(admin.ModelAdmin):
    model = Event
    ordering = ['created_on',]

admin.site.register(Event, EventAdmin)
