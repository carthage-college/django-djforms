from django.contrib import admin
from djforms.core.models import *

class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active', 'tags')

class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    search_fields = ('user__last_name','user__first_name','user__email','user__username',)

class PhotoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Department)
admin.site.register(GenericContactForm)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(GenericChoice, GenericChoiceAdmin)
