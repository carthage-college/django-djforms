# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from djforms.core.models import Department
from djforms.core.models import GenericChoice
from djforms.core.models import Photo
from djforms.core.models import Promotion
from djforms.core.models import UserProfile
from django_summernote.admin import SummernoteModelAdmin


class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active','tag_list')


class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    search_fields = (
        'user__last_name','user__first_name','user__email','user__username',
    )


class PhotoAdmin(admin.ModelAdmin):
    pass


class PromotionAdmin(SummernoteModelAdmin):
    raw_id_fields = ('user',)
    model = Promotion
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date_created', 'slug', 'amount', 'donors')
    summernote_fields = ('description', 'about', 'thank_you', 'email_info')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            self.prepopulated_fields = {}
            return self.readonly_fields + ('slug',)
        return self.readonly_fields


# django models
UserAdmin.list_display += ('id', 'last_login', 'date_joined')
UserAdmin.list_per_page = 500
# core models
admin.site.register(Department)
admin.site.register(GenericChoice, GenericChoiceAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
