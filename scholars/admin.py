from django.conf import settings
from django.contrib import admin
from djforms.scholars.models import *
from django.http import HttpResponse
from django.utils.encoding import smart_unicode, smart_str

import csv

def export_evs_requests(modeladmin, request, queryset):

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=celebration_of_scholars.csv'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Leader', 'Leader Email', 'Presenters', 'Funding Source', 'Work Type', 'Permission to Reproduce', 'Faculty Sponsor Approval', 'Table', 'Electricity', 'Link'])
    for p in queryset:
        link = "http://%s%s" % (settings.SERVER_URL,p.get_absolute_url())
        leader = "%s, %s" % (p.leader.last_name, p.leader.first_name)
        presenters = ""
        for f in p.presenters.all():
            if not f.leader:
                presenters += "%s, %s|" % (f.last_name, f.first_name)
            title = smart_str(p.title, encoding='utf-8', strings_only=False, errors='strict')
            funding = smart_str(p.funding, encoding='utf-8', strings_only=False, errors='strict')
            work_type = smart_str(p.work_type, encoding='utf-8', strings_only=False, errors='strict')
        writer.writerow([title, leader, p.user.email, presenters[:-1], funding, work_type, p.permission, p.shared, p.need_table, p.need_electricity, link])
    return response
export_evs_requests.short_description = "Export the selected Celebration of Scholars Submissions"

class PresentationAdmin(admin.ModelAdmin):
    model           = Presentation
    actions         = [export_evs_requests]
    raw_id_fields   = ("user","updated_by",)

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()


admin.site.register(Presenter)
admin.site.register(Presentation, PresentationAdmin)
