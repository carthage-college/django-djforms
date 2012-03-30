from django.contrib import admin
from djforms.processors.models import *

class OrderAdmin(admin.ModelAdmin):
    model = Order

    list_display  = ('last_name', 'first_name', 'email', 'time_stamp', 'status', 'auth', 'avs', 'cycle', 'payments', 'start_date')
    ordering      = ['contact__last_name', '-time_stamp','status','auth','avs','cycle','payments','start_date']
    list_filter   = ('status','auth','avs','cycle','payments')
    search_fields = ('email,', 'last_name', 'transid')
    raw_id_fields = ("contact",)

class ContactAdmin(admin.ModelAdmin):
    model = Contact

    list_display  = ('last_name', 'first_name', 'email', 'phone', 'address1', 'address2', 'city', 'state', 'postal_code')
    ordering      = ['last_name', 'city', 'state', 'postal_code']
    list_filter   = ('state',)
    search_fields = ('email,', 'last_name', 'phone', 'city', 'state', 'postal_code')

admin.site.register(Order, OrderAdmin)
admin.site.register(Contact, ContactAdmin)
