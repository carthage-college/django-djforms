from django.contrib import admin
from djforms.alumni.homecoming.models import HomecomingAttendee

class HomecomingAttendeeAdmin(admin.ModelAdmin):
    model = HomecomingAttendee
    list_display  = ('first_name', 'last_name', 'email',)
    search_fields = ('last_name', 'email',)
    ordering = ['created_on',]

admin.site.register(HomecomingAttendee, HomecomingAttendeeAdmin)
