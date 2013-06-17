from django.contrib import admin

from djforms.lis.conferences.course_ference.models import CourseFerenceAttender, CourseFerenceVendor

class CourseFerenceAdmin(admin.ModelAdmin):
    model = CourseFerenceAttender

    list_display  = ('last_name','first_name','email','job_title','affiliation','order_status','order_transid')
    ordering      = ['last_name','affiliation']
    search_fields = ('email,','last_name','affiliation','order_transid')

    list_max_show_all   = 500
    list_per_page       = 500

    def order_status(self, obj):
        try:
            stat = obj.order.all()[0].status
        except:
            stat = None
        return stat
    order_status.short_description = 'Transaction status'

    def order_transid(self, obj):
        try:
            tid = obj.order.all()[0].transid
        except:
            tid = None
        return tid
    order_transid.short_description = 'Transaction ID'

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        obj.save()

admin.site.register(CourseFerenceAttender, CourseFerenceAdmin)
admin.site.register(CourseFerenceVendor, CourseFerenceAdmin)

