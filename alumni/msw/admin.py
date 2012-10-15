from django.contrib import admin
from djforms.alumni.msw.models import ReunionContact

class ReunionContactAdmin(admin.ModelAdmin):
    model = ReunionContact
    list_display  = ('first_name', 'last_name', 'email',)
    search_fields = ('last_name', 'email',)
    ordering = ['created_at',]

admin.site.register(ReunionContact, ReunionContactAdmin)
