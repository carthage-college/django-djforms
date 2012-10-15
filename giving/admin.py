from django.contrib import admin

from djforms.giving.models import DonationContact
from djforms.processors.models import Order

class OrderInline(admin.TabularInline):
    model = DonationContact.order.through
    extra = 3

class DonationContactAdmin(admin.ModelAdmin):
    model = DonationContact

    list_display  = ('last_name', 'first_name', 'email', 'phone', 'address1', 'address2', 'city', 'state', 'postal_code')
    ordering      = ['last_name', 'city', 'state', 'postal_code']
    list_filter   = ('state',)
    search_fields = ('email,', 'last_name', 'phone', 'city', 'state', 'postal_code')
    #inlines = [OrderInline,]

admin.site.register(DonationContact, DonationContactAdmin)

