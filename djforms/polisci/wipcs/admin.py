from django.contrib import admin

from djforms.polisci.wipcs.models import RegistrationContact

class RegistrationContactAdmin(admin.ModelAdmin):
    model = RegistrationContact
    list_display = (
        'last_name', 'first_name', 'email', 'address1', 'address2', 'city',
        'state', 'postal_code', 'phone', 'submitting', 'payment_method',
        'order_status', 'order_transid', 'order_total'
    )
    exclude = (
        'country','second_name','previous_name','salutation'
    )
    ordering = ('-created_at',)
    list_filter = (
        'state','city'
    )
    search_fields = (
        'email,', 'last_name', 'city', 'state', 'postal_code'
    )
    raw_id_fields = ("order",)

    list_max_show_all = 500
    list_per_page = 500

    def order_status(self, obj):
        return '%s'%(obj.order.all()[0].status)
    order_status.short_description = 'Transaction status'

    def order_transid(self, obj):
        return '%s'%(obj.order.all()[0].transid)
    order_transid.short_description = 'Transaction ID'

    def order_total(self, obj):
        try:
            tid = obj.order.all()[0].total
        except:
            tid = None
        return tid
    order_total.short_description = 'Amount Paid'

admin.site.register(RegistrationContact, RegistrationContactAdmin)

