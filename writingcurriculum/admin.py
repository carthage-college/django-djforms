from django.contrib import admin
from djforms.writingcurriculum.models import *

class CriterionInline(admin.TabularInline):
    model = CourseProposal.criteria.through

class CourseProposalAdmin(admin.ModelAdmin):
    model = CourseProposal
    list_display  = ('course_title','course_number','department','academic_term','first_name', 'last_name', 'email', 'phone','approved_wi','workshop','permission')
    search_fields = ('course_title', 'description','objectives')
    ordering = ('-date_created',)
    raw_id_fields = ("user","updated_by",)
    inlines = [
        CriterionInline,
    ]
    exclude = ('criteria',)

    def save_model(self, request, obj):
        obj.updated_by = request.user
        obj.save()

admin.site.register(CourseProposal, CourseProposalAdmin)