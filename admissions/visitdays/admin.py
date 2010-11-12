from django.contrib import admin
from djforms.admissions.visitdays.models import VisitDayBaseProfile, VisitDayProfile, VisitDayEvent, VisitDay

class VisitDayProfileAdmin(admin.ModelAdmin):
    model = VisitDayProfile
    list_display  = ('first_name', 'last_name', 'email', 'phone', 'city', 'state','postal_code','gender')
    search_fields = ('last_name', 'email', 'city', 'state','postal_code','gender')

class VisitDayEventAdmin(admin.ModelAdmin):
    model = VisitDayEvent
    list_display = ('date','time','event','max_attendees','cur_attendees','active')
    ordering = ['date',]

admin.site.register(VisitDayBaseProfile, VisitDayProfileAdmin)
admin.site.register(VisitDayProfile, VisitDayProfileAdmin)
admin.site.register(VisitDayEvent, VisitDayEventAdmin)
admin.site.register(VisitDay)