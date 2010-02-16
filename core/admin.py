from django.contrib import admin
from djforms.core.models import *

class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active', 'tags')

class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)

class PhotoAdmin(admin.ModelAdmin):
    pass

admin.site.register(GenericContactForm)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(GenericChoice, GenericChoiceAdmin)
