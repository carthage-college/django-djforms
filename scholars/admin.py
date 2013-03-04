from django.contrib import admin
from djforms.scholars.models import *
from django.http import HttpResponse

import csv

def export_evs_requests(modeladmin, request, queryset):

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=celebration_of_scholars.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Title', 'First Name', 'Last Name', 'Email', 'Funding Source', 'Work Type', 'Permission to Reproduce', 'Faculty Sponsor Approval', 'Link', 'Abstract'])
    for p in queryset:
        writer.writerow([p.id, p.title, p.leader.first_name, p.leader.last_name, p.user.email, p.funding, p.work_type, p.permission, p.shared, p.get_absolute_url(), p.abstract_text])
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
