from django.contrib import admin
from djforms.characterquest.models import EnrollmentProfile

class EnrollmentProfileAdmin(admin.ModelAdmin):
    model = EnrollmentProfile
    list_display  = ('first_name', 'last_name', 'email', 'phone', 'city', 'state','zip','sex')
    raw_id_fields = ('profile',)
    search_fields = ('last_name', 'email', 'city', 'state','zip','sex')

admin.site.register(EnrollmentProfile, EnrollmentProfileAdmin)
