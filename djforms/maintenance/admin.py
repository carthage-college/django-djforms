from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

from djforms.maintenance.models import *
from djforms.core.models import Photo

import csv

# disable authority permissions from the admin
#admin.site.disable_action('edit_permissions')

def export_evs_requests(modeladmin, request, queryset):

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=evs_export.csv'
    writer = csv.writer(response)
    writer.writerow([
        'Building Name', 'Room Number', 'Type of Request', 'Description',
        'Date Created', 'Damage Charge', 'First Name', 'Last Name',
        'Email', 'Phone', 'Status', 'Date Completed'
    ])
    for evs in queryset:
        writer.writerow([
            evs.building.name,evs.room_number,evs.type_of_request,
            evs.description,evs.date_created,evs.damage_charge,
            evs.user.first_name,evs.user.last_name,evs.user.email,
            evs.user.get_profile().phone,evs.status,evs.date_completed
        ])
    return response
export_evs_requests.short_description = "Export EVS Maintenance Requests"


class MaintenanceRequestAdmin(admin.ModelAdmin):
    model = MaintenanceRequest
    list_display  = (
        'id', 'building_name', 'room_number', 'type_of_request',
        'date_created', 'damage_charge', 'last_name', 'first_name',
        'email', 'phone', 'photo_link', 'status'
    )
    ordering = [
        '-id','building','type_of_request','date_created',
        'user__last_name','user__email','status'
    ]
    search_fields = ('building__name', 'room_number', 'type_of_request__name')
    actions       = [export_evs_requests]
    raw_id_fields = ("user","updated_by","photo")
    list_per_page = 500

    def photo_link(self, instance):
        code = None
        if instance.photo:
            code = '<a href="{}" target="_blank">Photo</a>'.format(
                instance.photo.original.url
            )
        return code
    photo_link.allow_tags = True
    photo_link.short_description = "Photo"

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()

admin.site.register(MaintenanceRequest, MaintenanceRequestAdmin)
