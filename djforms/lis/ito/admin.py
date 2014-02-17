from django.contrib import admin
from djforms.lis.ito.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display  = ('first_name', 'last_name', 'email',)
    search_fields = ('last_name', 'email',)
    ordering = ['created_on',]

admin.site.register(Profile, ProfileAdmin)
