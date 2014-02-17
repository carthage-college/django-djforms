from django.contrib import admin
from djforms.video.models import Contest

class ContestAdmin(admin.ModelAdmin):
    model = Contest
    list_display  = ('title','first_name', 'last_name', 'email',)
    search_fields = ('last_name', 'email',)
    ordering = ['created_on',]

admin.site.register(Contest, ContestAdmin)
