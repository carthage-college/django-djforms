from django.contrib import admin

from djforms.lis.conferences.registration.models import RegistrationContact

class RegistrationContactAdmin(admin.ModelAdmin):
    model = RegistrationContact

    list_display  = ('last_name', 'first_name', 'email', 'phone', 'address1', 'address2', 'city', 'state', 'postal_code')
    ordering      = ['last_name', 'city', 'state', 'postal_code']
    list_filter   = ('state',)
    search_fields = ('email,', 'last_name', 'phone', 'city', 'state', 'postal_code')

admin.site.register(RegistrationContact, RegistrationContactAdmin)

