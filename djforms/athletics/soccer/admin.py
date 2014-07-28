from django.contrib import admin

from djforms.athletics.soccer.models import SoccerCampAttender

import datetime

class SoccerCampAttenderAdmin(admin.ModelAdmin):
    model = SoccerCampAttender
    exclude       = ('country','second_name','previous_name','salutation')
    raw_id_fields = ('order',)

    list_display  = (
        'last_name','first_name','created_at','dob','age','football',
        'gender','address1','address2','city','state','postal_code','phone',
        'email','order_transid','order_status','parent_guard','roommate',
        'dorm','years_attend','goalkeeper','shirt_size','session','reg_fee',
        'amount','order_total', 'payment_method'
    )
    ordering      = ('-created_at',)
    search_fields = ('last_name','email','postal_code')

    list_max_show_all   = 500
    list_per_page       = 500

    def queryset(self, request):
        """
        only show registrations that were created after a certain date.
        they wanted to delete old registrations to make the dashboard
        more manageable but we can't do that so we just hide them.
        """
        TODAY = datetime.date.today()
        YEAR = int(TODAY.year)
        MES = int(TODAY.month)
        DAY = int(TODAY.day)
        qs = super(SoccerCampAttenderAdmin, self).queryset(request)
        if MES <= 7 and DAY <= 21:
            YEAR = YEAR - 1
        start_date = datetime.date(YEAR, 7, 21)
        return qs.filter(created_at__gte=start_date)

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
    order_total.short_description = 'Amount Paid'

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()

admin.site.register(SoccerCampAttender, SoccerCampAttenderAdmin)

