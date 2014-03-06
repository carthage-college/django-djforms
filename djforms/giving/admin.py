from django.contrib import admin

from djforms.giving.models import DonationContact
from djforms.processors.models import Order

class OrderInline(admin.TabularInline):
    model = DonationContact.order.through
    extra = 3

class DonationContactAdmin(admin.ModelAdmin):
    model = DonationContact
    exclude       = ('country','second_name','previous_name','salutation')
    raw_id_fields = ('order',)

    ordering      = ['last_name', 'city', 'state', 'postal_code']
    search_fields = ('last_name', 'phone', 'city', 'state', 'postal_code')
    #inlines = [OrderInline,]

    list_display  = (
        'last_name','first_name','created_at','email','phone',
        'address1','address2','city','state','postal_code',
        'spouse','relation','class_of','matching_company',
        'order_promo',
        'order_cycle','order_payments','order_start_date',
        'order_transid','order_status','order_total',
        'order_comments','opt_in'
    )

    def order_promo(self, obj):
        try:
            promo = obj.order.all()[0].promotion
        except:
            promo = None
        return promo
    order_promo.short_description = 'Campaign'

    def order_status(self, obj):
        try:
            stat = obj.order.all()[0].status
        except:
            stat = None
        return stat
    order_status.short_description = 'Transaction status'

    def order_transid(self, obj):
        try:
            tid = obj.order.all()[0].transid
        except:
            tid = None
        return tid
    order_transid.short_description = 'Transaction ID'

    def order_total(self, obj):
        try:
            tid = obj.order.all()[0].total
        except:
            tid = None
        return tid
    order_total.short_description = 'Donation'

    def order_cycle(self, obj):
        try:
            cycle = obj.order.all()[0].cycle
        except:
            cycle = None
        return cycle
    order_cycle.short_description = 'Interval'

    def order_payments(self, obj):
        try:
            payments = obj.order.all()[0].payments
        except:
            payments = None
        return payments
    order_payments.short_description = 'Duration'

    def order_start_date(self, obj):
        try:
            sdate = obj.order.all()[0].start_date
        except:
            sdate = None
        return sdate
    order_start_date.short_description = 'Start Date'

    def order_comments(self, obj):
        try:
            com = obj.order.all()[0].comments
        except:
            com = None
        return com
    order_comments.short_description = 'Designation'

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()

admin.site.register(DonationContact, DonationContactAdmin)
