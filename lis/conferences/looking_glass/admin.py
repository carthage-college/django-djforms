from django.contrib import admin

from djforms.lis.conferences.looking_glass.models import RegistrationContact

class RegistrationContactAdmin(admin.ModelAdmin):
    model = RegistrationContact

    list_display  = ('last_name', 'first_name', 'name_tag', 'email', 'address1', 'address2', 'city', 'state', 'postal_code','affiliation')
    ordering      = ['last_name', 'city', 'state', 'postal_code', 'affiliation']
    list_filter   = ('state','city')
    search_fields = ('email,', 'last_name', 'city', 'state', 'postal_code','affiliation')

admin.site.register(RegistrationContact, RegistrationContactAdmin)

