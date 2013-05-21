from django.contrib import admin
from models import *

class OrderAdmin(admin.ModelAdmin):
    model = Order

    list_display  = ('last_name', 'contact_name', 'email', 'operator', 'promotion', 'time_stamp', 'status', 'auth', 'cycle', 'payments', 'start_date','transid')
    ordering      = ['promotion', '-time_stamp','status','auth','avs','cycle','payments','start_date']
    list_filter   = ('status','auth','avs','cycle','payments','promotion')
    search_fields = ('transid',)
    raw_id_fields = ('promotion',)

    def contact_name(self, obj):
        return '<strong><a href="%s%s/">%s</a></strong>' % ('/forms/admin/processors/contact/', obj.cid(), obj.first_name())
    contact_name.allow_tags = True
    contact_name.short_description = 'First name (contact info)'

def invoice_url(self, obj):
    return '<a href="%s">%s</a>' % (obj.firm_url, obj.firm_url)
invoice_url.allow_tags = True


class ContactAdmin(admin.ModelAdmin):
    model = Contact

    list_display  = ('last_name', 'first_name', 'email', 'phone', 'address1', 'address2', 'city', 'state', 'postal_code')
    ordering      = ['last_name', 'city', 'state', 'postal_code']
    list_filter   = ('state',)
    search_fields = ('last_name', 'phone', 'city', 'state', 'postal_code')

admin.site.register(Order, OrderAdmin)
admin.site.register(Contact, ContactAdmin)
