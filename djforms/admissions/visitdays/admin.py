# -*- coding: utf-8 -*-

import csv

from django.contrib import admin
from django.http import HttpResponse

from djforms.admissions.visitdays.models import VisitDay
from djforms.admissions.visitdays.models import VisitDayBaseProfile
from djforms.admissions.visitdays.models import VisitDayEvent
from djforms.admissions.visitdays.models import VisitDayProfile


def export_profiles(modeladmin, request, queryset):
    """Export visit day profile data to CSV file."""

    response = HttpResponse("", content_type="text/csv; charset=utf-8")
    response['Content-Disposition'] = 'attachment; filename=visit_day_profiles.csv'
    writer = csv.writer(response)
    writer.writerow(
        [
            'first name',
            'last name',
            'email',
            'mobile',
            'phone',
            'address',
            'city',
            'state',
            'zip',
            'gender',
            'date',
            'guardian email',
            'guardian type',
            'event title',
        ]
    )
    for c in queryset:
        row = [
            c.first_name.encode('utf-8'),
            c.last_name.encode('utf-8'),
            c.email,
            c.mobile,
            c.phone,
            c.address.encode('utf-8'),
            c.city.encode('utf-8'),
            c.state.encode('utf-8'),
            c.postal_code,
            c.gender,
            c.date,
            c.guardian_email,
            c.guardian_type,
            c.event_title().encode('utf-8'),
        ]

        writer.writerow(row)
    return response

export_profiles.short_description = "Export the selected profiles"


class VisitDayProfileAdmin(admin.ModelAdmin):
    model = VisitDayProfile
    list_display  = (
        'first_name',
        'last_name',
        'email',
        'mobile',
        'phone',
        'city',
        'state',
        'postal_code',
        'gender',
        'date',
        'guardian_email',
        'guardian_type',
        'event_title',
    )
    search_fields = (
        'last_name',
        'city',
        'state',
        'postal_code',
        'gender',
        'date__date',
        'date__event__title',
    )
    #list_filter = ('date__date',)
    date_hierarchy = 'date__date'
    list_max_show_all   = 200
    list_per_page       = 200
    actions             = [export_profiles]


class VisitDayEventAdmin(admin.ModelAdmin):
    model = VisitDayEvent
    list_display = (
        'date',
        'time',
        'event',
        'max_attendees',
        'cur_attendees',
        'active',
    )
    ordering = ['-date']


admin.site.register(VisitDayProfile, VisitDayProfileAdmin)
admin.site.register(VisitDayEvent, VisitDayEventAdmin)
admin.site.register(VisitDay)
