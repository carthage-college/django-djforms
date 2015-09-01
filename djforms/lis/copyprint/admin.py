from django.contrib import admin
from djforms.lis.copyprint.models import CardRequest

class CardRequestAdmin(admin.ModelAdmin):
    model = CardRequest
    list_display  = ('last_name', 'first_name', 'email', 'entity_name')
    raw_id_fields = ('user',)
    search_fields = ('last_name', 'email', 'entity_name')

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        obj.save()

admin.site.register(CardRequest, CardRequestAdmin)
