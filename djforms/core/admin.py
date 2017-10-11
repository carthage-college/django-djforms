from django import forms
from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _
from djforms.core.models import *

from djforms.core.models import GenericChoice


class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active', 'tags')


class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = (
        'user__last_name','user__first_name','user__email','user__username',
    )


class PhotoAdmin(admin.ModelAdmin):
    pass


class PromotionAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    model = Promotion
    prepopulated_fields = {'slug': ('title',)}


# core models
admin.site.register(Department)
admin.site.register(GenericChoice, GenericChoiceAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
