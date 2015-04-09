from django.contrib import admin

from djforms.athletics.soccer.models import SoccerCampAttender
from djforms.core.util import export_as_csv_action

import datetime
import csv

'''
def export_attenders(modeladmin, request, queryset):
    # exclude these fields from registration data
    #exclude = ['id','user']
    response = HttpResponse("", content_type="text/csv; charset=utf-8")
    filename = "{}.csv".format(modeladmin)
    response['Content-Disposition']='attachment; filename={}'.format(filename)
    writer = csv.writer(response)
    for reg in queryset:
        writer.writerow(fields)
    return response

export_attenders.short_description = "Export Soccer Camp Attenders"
'''

class SoccerCampAttenderAdmin(admin.ModelAdmin):
    model = SoccerCampAttender
    exclude       = ('country','second_name','previous_name','salutation')
    raw_id_fields = ('order',)
    actions = [export_as_csv_action(header=True)]

    list_display  = (
        'last_name','first_name','created_at','dob','age','football',
        'gender','address1','address2','city','state','postal_code','phone',
        'email','order_transid','order_status','parent_guard','roommate',
        'dorm','years_attend','goalkeeper','shirt_size','session','reg_fee',
        'amount','order_total', 'payment_method',
        'medical_history','assumption_risk','insurance_card_links'
    )
    ordering      = ('-created_at',)
    search_fields = ('last_name','email','postal_code')

    list_max_show_all   = 500
    list_per_page       = 500
    list_editable = [
        'medical_history','assumption_risk'
    ]

    def insurance_card_links(self, instance):
        try:
            code = '''
                <a href="{}" target="_blank">Front</a> |
                <a href="{}" target="_blank">Back</a>
            '''.format(
                instance.insurance_card_front.url,
                instance.insurance_card_back.url
            )
        except:
            code = None
        return code
    insurance_card_links.allow_tags = True
    insurance_card_links.short_description = "Insurance Card Files"

    def queryset(self, request):
        """
        only show registrations that were created after a certain date.
        they wanted to delete old registrations to make the dashboard
        more manageable but we can't do that so we just hide them.
        """
        TODAY = datetime.date.today()
        YEAR = int(TODAY.year)
        MES = int(TODAY.month)
        #DAY = int(TODAY.day)
        qs = super(SoccerCampAttenderAdmin, self).queryset(request)
        if MES <= 8:
            YEAR = YEAR - 1
        start_date = datetime.date(YEAR, 8, 1)
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

