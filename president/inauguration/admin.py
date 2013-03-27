from django.contrib import admin
from djforms.president.inauguration.models import RsvpContact

class RsvpContactAdmin(admin.ModelAdmin):
    model = RsvpContact
    list_display  = ('first_name', 'last_name', 'email',)
    search_fields = ('last_name', 'email',)
    ordering = ['created_at',]

admin.site.register(RsvpContact, RsvpContactAdmin)
