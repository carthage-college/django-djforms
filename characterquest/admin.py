from django.contrib import admin
from djforms.characterquest.models import ApplicationProfile

class ApplicationProfileAdmin(admin.ModelAdmin):
    model = ApplicationProfile
    list_display  = ('first_name', 'last_name', 'email', 'phone', 'city', 'state','zip','gender')
    raw_id_fields = ('profile',)
    search_fields = ('last_name', 'email', 'city', 'state','zip','gender')

admin.site.register(ApplicationProfile, ApplicationProfileAdmin)
