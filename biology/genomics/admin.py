from django.contrib import admin
from djforms.biology.genomics.models import PhageHunter

class PhageHunterAdmin(admin.ModelAdmin):
    model = PhageHunter
    list_display  = ('first_name', 'last_name', 'email',)
    search_fields = ('last_name', 'email',)
    ordering = ['created_on',]

admin.site.register(PhageHunter, PhageHunterAdmin)
