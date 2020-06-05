from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse

from djforms.athletics.soccer.models import SoccerCampAttender

import datetime
import csv


def export_attenders(modeladmin, request, queryset):
    """Export soccer camp attenders to CSV."""
    field_names = [
        'last_name',
        'first_name',
        'created_at',
        'dob',
        'age',
        'football',
        'gender',
        'address1',
        'city',
        'state',
        'postal_code',
        'phone',
        'email',
        'order',
        'parent_guard',
        'roommate',
        'dorm',
        'years_attend',
        'goalkeeper',
        'shirt_size',
        'session',
        'amount',
        'payment_method',
        'reg_fee',
        'medical_history',
        'assumption_risk',
        'insurance_card_links',
    ]

    headers = [
        'last_name',
        'first_name',
        'created_at',
        'dob',
        'age',
        'football',
        'gender',
        'address1',
        'city',
        'state',
        'postal_code',
        'phone',
        'email',
        'order_total',
        'order_transid',
        'order_status',
        'parent_guard',
        'roommate',
        'dorm',
        'years_attend',
        'goalkeeper',
        'shirt_size',
        'session',
        'amount',
        'payment_method',
        'reg_fee',
        'medical_history',
        'assumption_risk',
        'insurance_card_links',
    ]

    response = HttpResponse("", content_type='text/csv; charset=utf-8')
    filename = 'soccer_soccercampattenders.csv'
    response['Content-Disposition']='attachment; filename={0}'.format(filename)
    writer = csv.writer(response)
    writer.writerow(headers)
    for reg in queryset:
        fields = []
        for field in field_names:
            if field == 'order':
                # if, somehow, a transaction comes through w/out these three
                try:
                    transid = reg.order.all()[0].transid
                    status = reg.order.all()[0].status
                    total = reg.order.all()[0].total
                except:
                    transid=''
                    status=''
                    total=''
                fields.append(transid)
                fields.append(status)
                fields.append(total)
            else:
                fields.append(
                    unicode(getattr(reg, field, None)).encode('utf-8', 'ignore')
                )
        writer.writerow(fields)
    return response

export_attenders.short_description = "Export Soccer Camp Attenders"


class SoccerCampAttenderAdmin(admin.ModelAdmin):
    model = SoccerCampAttender
    exclude       = ('country', 'second_name', 'previous_name', 'salutation')
    raw_id_fields = ('order',)
    actions = [export_attenders]

    list_display  = (
        'last_name',
        'first_name',
        'created_at',
        'dob',
        'age',
        'football',
        'gender',
        'address1',
        'city',
        'state',
        'postal_code',
        'phone',
        'email',
        'order_transid',
        'order_status',
        'parent_guard',
        'roommate',
        'dorm',
        'years_attend',
        'goalkeeper',
        'shirt_size',
        'session',
        'reg_fee',
        'amount',
        'order_total',
        'payment_method',
        'medical_history',
        'assumption_risk',
        'insurance_card_links',
    )
    ordering      = ('-created_at',)
    search_fields = ('last_name', 'email', 'postal_code')

    list_max_show_all   = 1000
    list_per_page       = 1000
    list_editable = ['medical_history', 'assumption_risk']

    def insurance_card_links(self, instance):
        try:
            code = '''
                <a href="{0}" target="_blank">Front</a> |
                <a href="{1}" target="_blank">Back</a>
            '''.format(
                instance.insurance_card_front.url,
                instance.insurance_card_back.url,
            )
        except:
            code = None
        return code
    insurance_card_links.allow_tags = True
    insurance_card_links.short_description = "Insurance Card Files"

    def get_queryset(self, request):
        """
        only show registrations that were created after a certain date.
        they wanted to delete old registrations to make the dashboard
        more manageable but we can't do that so we just hide them.
        """
        TODAY = datetime.date.today()
        YEAR = int(TODAY.year)
        MES = int(TODAY.month)
        #DAY = int(TODAY.day)
        qs = super(SoccerCampAttenderAdmin, self).get_queryset(request)
        if MES < settings.SOCCER_CAMP_MONTH:
            YEAR = YEAR - 1
        start_date = datetime.date(YEAR, 8, settings.SOCCER_CAMP_DAY)
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
