from django.contrib import admin
from djforms.sustainability.green.models import Pledge

class PledgeAdmin(admin.ModelAdmin):
    model = Pledge
    list_display  = ('first_name', 'last_name', 'email',)
    search_fields = ('last_name', 'email',)
    ordering = ['-id',]
    raw_id_fields = ("user",)

admin.site.register(Pledge, PledgeAdmin)
