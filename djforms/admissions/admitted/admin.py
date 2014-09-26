from django.contrib import admin
from django.http import HttpResponse

from djforms.admissions.admitted.models import Candidate

import csv

def export_candidates(modeladmin, request, queryset):

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=will_i_be_admitted.csv'
    writer = csv.writer(response)
    writer.writerow(
        [
            'First name', 'email', 'status', 'act/stat', 'GPA', 'GPA scale',
            'Adjusted GPA', 'Information', 'Prospect status', 'Created',
            'Updated'
        ]
    )
    for c in queryset:
        writer.writerow(
            [
                c.first_name, c.email, c.status, c.act_sat, c.gpa, c.gpa_scale,
                c.adjusted_gpa, c.information, c.prospect_status,c.created_on,
                c.updated_on
            ]
        )
    return response
export_candidates.short_description = """
    Export the selected Candidates for admissions to Carthage
"""

class CandidateAdmin(admin.ModelAdmin):
    model = Candidate

    list_display  = (
        'first_name','email','status','act_sat','gpa','gpa_scale',
        'adjusted_gpa','prospect_status','created_on'
    )
    ordering = [
        'created_on','first_name','email','status','prospect_status'
    ]
    search_fields = (
        'email','first_name','prospect_status'
    )

    list_max_show_all   = 500
    list_per_page       = 500
    actions             = [export_candidates]

admin.site.register(Candidate, CandidateAdmin)
