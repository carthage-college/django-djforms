from django.contrib import admin

from djforms.lis.conferences.looking_glass.models import RegistrationContact

class RegistrationContactAdmin(admin.ModelAdmin):
    model = RegistrationContact

    list_display  = ('last_name', 'first_name', 'name_tag', 'email', 'address1', 'address2', 'city', 'state', 'postal_code','affiliation', 'order_status', 'order_transid')
    ordering      = ['last_name', 'city', 'state', 'postal_code', 'affiliation',]
    list_filter   = ('state','city')
    search_fields = ('email,', 'last_name', 'city', 'state', 'postal_code','affiliation')

    def order_status(self, obj):
        return '%s'%(obj.order.all()[0].status)
    order_status.short_description = 'Transaction status'

    def order_transid(self, obj):
        return '%s'%(obj.order.all()[0].transid)
    order_transid.short_description = 'Transaction ID'

admin.site.register(RegistrationContact, RegistrationContactAdmin)

