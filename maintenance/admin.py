from django.contrib import admin
from djforms.maintenance.models import *
from django.http import HttpResponse

import csv

# disable authority permissions from the admin
#admin.site.disable_action('edit_permissions')

def export_evs_requests(modeladmin, request, queryset):

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=evs_export.csv'
    writer = csv.writer(response)
    writer.writerow(['Building Name', 'Room Number', 'Type of Request', 'Description', 'Date Created', 'Damage Charge', 'First Name', 'Last Name', 'Email', 'Phone', 'Status', 'Date Completed'])
    for evs in queryset:
        writer.writerow([evs.building.name,evs.room_number,evs.type_of_request,evs.description,evs.date_created,evs.damage_charge,evs.user.first_name,evs.user.last_name,evs.user.email,evs.user.get_profile().phone,evs.status,evs.date_completed])
    return response
export_evs_requests.short_description = "Export the selected EVS Maintenance Requests"

class MaintenanceRequestAdmin(admin.ModelAdmin):
    model = MaintenanceRequest
    list_display  = ('building_name', 'room_number', 'type_of_request', 'date_created', 'damage_charge', 'first_name', 'last_name', 'email', 'phone', 'status')
    #list_filter   = ('building_name', 'type_of_request')
    search_fields = ('building__name', 'room_number', 'type_of_request__name')
    actions       = [export_evs_requests]
    raw_id_fields = ("user","updated_by",)

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()

admin.site.register(MaintenanceRequest, MaintenanceRequestAdmin)
