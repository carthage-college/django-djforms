# -*- coding: utf-8 -*-

from django.contrib import admin
from djforms.alumni.memory.models import Questionnaire
from djforms.core.util import export_as_csv_action


class PhotoInline(admin.TabularInline):
    model = Questionnaire.photos.through
    extra = 5


class QuestionnaireAdmin(admin.ModelAdmin):
    model = Questionnaire
    list_display  = (
        'first_name',
        'last_name',
        'email',
        'phone',
        'city',
        'state',
        'postal_code',
        'class_year',
        'created_at',
    )
    list_max_show_all   = 500
    list_per_page       = 500
    list_editable = ['class_year']
    search_fields = ('last_name', 'email', 'city', 'state','postal_code')
    ordering = ('-created_at',)
    inlines = [PhotoInline,]
    exclude = ('photos',)
    actions = [export_as_csv_action(header=True)]


admin.site.register(Questionnaire, QuestionnaireAdmin)
