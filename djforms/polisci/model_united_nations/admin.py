from django.contrib import admin

from models import Attender, Country

class AttenderAdmin(admin.ModelAdmin):
    model = Attender
    exclude = ('country','order','second_name','previous_name','salutation')
    raw_id_fields = ('order',)

    list_display  = (
        'last_name','first_name','school_name','office','created_at',
        'address1','address2','city','state','postal_code','phone',
        'email','number_of_del','number_of_stu',
        'delegation_1','delegation_2','delegation_3',
        'delegation_4','delegation_5'
    )
    ordering = ('-created_at',)
    search_fields = ('last_name','email','postal_code')

    list_max_show_all = 500
    list_per_page = 500

admin.site.register(Attender, AttenderAdmin)
admin.site.register(Country)

