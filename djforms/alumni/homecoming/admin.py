from django.contrib import admin
from djforms.alumni.homecoming.models import Attendee

class AttendeeAdmin(admin.ModelAdmin):
    model = Attendee
    list_display  = ('first_name', 'last_name', 'email','grad_class')
    search_fields = ('last_name', 'email','grad_class')
    ordering = ['created_at','grad_class']

admin.site.register(Attendee, AttendeeAdmin)
