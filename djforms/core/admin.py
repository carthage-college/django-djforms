from django.contrib import admin
from djforms.core.models import *

class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active', 'tags')

class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    search_fields = ('user__last_name','user__first_name','user__email','user__username',)

class PhotoAdmin(admin.ModelAdmin):
    pass

class PromotionAdmin(admin.ModelAdmin):
    model = Promotion
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Department)
admin.site.register(GenericContactForm)
admin.site.register(GenericChoice, GenericChoiceAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)