# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from djforms.core.models import Department
from djforms.core.models import GenericChoice
from djforms.core.models import Photo
from djforms.core.models import Promotion
from djforms.core.models import UserProfile


class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active','tag_list')


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
    list_display = ('title', 'date_created', 'slug', 'amount', 'donors')


# core models
admin.site.register(Department)
admin.site.register(GenericChoice, GenericChoiceAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
