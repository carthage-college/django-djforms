from django.contrib import admin
from djforms.core.models import *

class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active', 'tags')

admin.site.register(GenericContactForm)
admin.site.register(GenericChoice, GenericChoiceAdmin)
