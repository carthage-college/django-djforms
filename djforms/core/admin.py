from django import forms
from django.contrib import admin
from django.utils.translation import ugettext, ugettext_lazy as _
from djforms.core.models import *

from djforms.core.models import GenericChoice

from tagging.models import Tag, TaggedItem

mrt = Tag.objects.get(name__iexact='Maintenance Request Type')
bld = Tag.objects.get(name__iexact='Building Name')

PERMISSION = TaggedItem.objects.get_union_by_model(
    GenericChoice, [mrt, bld]
).filter(active=True).order_by('name')


class UserProfileAdminForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserProfileAdminForm, self).__init__(*args, **kwargs)
        self.fields['permission'].queryset = PERMISSION


class GenericChoiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'ranking', 'active', 'tags')


class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileAdminForm
    filter_horizontal = ('permission',)
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
