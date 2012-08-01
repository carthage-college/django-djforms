from django.contrib import admin
from djforms.music.ensembles.choral.models import Candidate, TimeSlot

class CandidateAdmin(admin.ModelAdmin):
    model = Candidate
    # configs
    ordering        = ['user__last_name','created_on','grad_year',]
    list_display    = ('first_name', 'last_name', 'email','majors','grad_year','ensemble','time_slot')
    raw_id_fields   = ('user',)
    search_fields   = ('user__last_name','user__first_name','user__email',)

class TimeSlotAdmin(admin.ModelAdmin):
    model = TimeSlot
    list_display    = ('date_time', 'active')
    ordering        = ['date_time','active',]

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)

