# -*- coding: utf-8 -*-

import csv
import datetime

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse
from django.utils.encoding import smart_str
from djforms.scholars.models import *


def export_scholars(modeladmin, request, queryset):
    """Export the presentation data."""
    response = HttpResponse('', content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename=cos.csv'
    writer = csv.writer(response)
    writer.writerow([
        'Title',
        'Reviewer',
        'Leader',
        'Leader Email',
        'Sponsor',
        'Other Sponsor',
        'Presenters',
        'Funding Source',
        'Work Type',
        'Permission to Reproduce',
        'Faculty Sponsor Approval',
        'Presentation Type',
        'Table',
        'Electricity',
        'Link',
        'Poster',
        'Date created',
    ])
    for presentation in queryset:
        link = 'http://{0}{1}'.format(
            settings.SERVER_URL,
            presentation.get_absolute_url(),
        )
        poster = 'http://{0}/assets/{1}'.format(
            settings.SERVER_URL, presentation.poster_file,
        )
        try:
            leader = '{0}, {1}'.format(
                presentation.leader.last_name,
                presentation.leader.first_name,
            )
        except Exception:
            leader = ''
        presenters = ''
        for presenter in presentation.presenters.all():
            if not presenter.leader:
                presenters += '{0}, {1}|'.format(
                    presenter.last_name, presenter.first_name,
                )
            title = smart_str(
                presentation.title,
                encoding='utf-8',
                strings_only=False,
                errors='strict',
            )
            funding = smart_str(
                presentation.funding,
                encoding='utf-8',
                strings_only=False,
                errors='strict',
            )
            work_type = smart_str(
                presentation.work_type,
                encoding='utf-8',
                strings_only=False,
                errors='strict',
            )
        sponsor_email = ''
        if presentation.leader:
            sponsor_email = presentation.leader.sponsor_email
            sponsor_other = presentation.leader.sponsor_other
        writer.writerow([
            title,
            presentation.reviewer,
            leader,
            presentation.user.email,
            sponsor_email,
            sponsor_other,
            presenters[:-1],
            funding,
            work_type,
            presentation.permission,
            presentation.shared,
            presentation.presentation_type,
            presentation.need_table,
            presentation.need_electricity,
            link,poster,
            presentation.date_created,
        ])
    return response
export_scholars.short_description = """
    Export the selected Celebration of Scholars Submissions
"""


class PresentationAdmin(admin.ModelAdmin):
    """Admin class for the presentation data model."""

    model = Presentation
    actions = [export_scholars]
    raw_id_fields = ('user', 'updated_by', 'leader')
    list_max_show_all = 500
    list_per_page = 500
    list_display = (
        'title',
        'reviewer',
        'last_name',
        'first_name',
        'email',
        'sponsor',
        'sponsor_other',
        'get_presenters',
        'funding',
        'work_type',
        'permission',
        'shared',
        'presentation_type',
        'need_table',
        'need_electricity',
        'status',
        'poster',
        'date_created',
    )
    ordering = [
        '-date_created',
        'title',
        'work_type',
        'permission',
        'shared',
        'presentation_type',
        'need_table',
        'need_electricity',
        'status',
    ]
    search_fields = (
        'title',
        'user__last_name',
        'user__email',
        'funding',
    )
    list_filter = ('status', 'date_created')
    list_editable = ['reviewer']

    def queryset(self, request):
        """Only show presentations that were created after a certain date."""
        TODAY = datetime.date.today()
        YEAR = int(TODAY.year)
        qs = super(PresentationAdmin, self).queryset(request)
        start_date = datetime.date(YEAR, 1, 1)
        return qs.filter(date_created__gte=start_date)

    def save_model(self, request, obj, form, change):
        """Override the save method to update some things."""
        if change:
            obj.updated_by = request.user
        obj.save()


class PresenterAdmin(admin.ModelAdmin):
    """Admin class for the presenter model."""

    model = Presenter
    list_max_show_all = 500
    list_per_page = 500
    list_display = (
        'date_created',
        'last_name',
        'first_name',
        'email',
        'leader',
        'prez_type',
        'college_year',
        'major',
        'hometown',
        'sponsor',
        'sponsor_name',
        'sponsor_email',
        'sponsor_other',
        'department',
    )
    ordering = [
        'date_created',
        'last_name',
        'first_name',
        'email',
        'leader',
        'prez_type',
        'college_year',
        'major',
        'hometown',
        'sponsor',
        'sponsor_name',
        'sponsor_email',
        'sponsor_other',
        'department',
    ]
    search_fields = (
        'last_name',
        'first_name',
        'email',
    )


admin.site.register(Presenter, PresenterAdmin)
admin.site.register(Presentation, PresentationAdmin)
