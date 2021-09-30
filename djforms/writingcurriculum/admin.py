# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from djforms.writingcurriculum.models import *


class CourseCriteriaForm(forms.ModelForm):

    class Meta:
        model = CourseCriteria
        fields = '__all__'


class CriteriaInline(admin.TabularInline):

    model = CourseProposal.criteria.through
    extra = 5


class CourseCriteriaAdmin(admin.ModelAdmin):

    form =  CourseCriteriaForm
    fieldsets = (
        (None, {
            'fields': (
                'type_assignment', 'number_pages',
                'percent_grade', 'description'
            )
        }),
    )


class CourseProposalAdmin(admin.ModelAdmin):

    model = CourseProposal
    list_display  = (
        'course_title',
        'date_created',
        'course_number',
        'department',
        'academic_term',
        'first_name',
        'last_name',
        'email',
        'phone',
        'approved_wi',
        'workshop',
        'permission',
    )
    search_fields = ('course_title', 'description', 'objectives')
    ordering = ['-date_created']
    raw_id_fields = ('user', 'updated_by')
    inlines = [CriteriaInline]
    exclude = ['criteria']

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()


admin.site.register(CourseCriteria, CourseCriteriaAdmin)
admin.site.register(CourseProposal, CourseProposalAdmin)
