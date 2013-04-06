from django.contrib import admin

from djforms.lis.conferences.course_ference.models import CourseFerenceAttender, CourseFerenceVendor

class CourseFerenceAdmin(admin.ModelAdmin):
    model = CourseFerenceAttender

    list_display  = ('last_name', 'first_name', 'email', 'address1', 'address2', 'city', 'state', 'postal_code')
    ordering      = ['last_name', 'city', 'state', 'postal_code']
    list_filter   = ('state',)
    search_fields = ('email,', 'last_name', 'city', 'state', 'postal_code')

admin.site.register(CourseFerenceAttender, CourseFerenceAdmin)
admin.site.register(CourseFerenceVendor, CourseFerenceAdmin)

