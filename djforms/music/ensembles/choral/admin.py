# -*- coding: utf-8 -*-

from django.contrib import admin
from djforms.music.ensembles.choral.models import Candidate
from djforms.music.ensembles.choral.models import TimeSlot


class CandidateAdmin(admin.ModelAdmin):
    """Admin model for the choral tryout candidate."""

    model = Candidate
    ordering = ('-created_on', 'user__last_name')
    list_display = (
        'first_name',
        'last_name',
        'email',
        'time_slot',
        'majors',
        'grad_year',
        'created_on',
        'experience',
    )
    raw_id_fields = ['user']
    search_fields = ('user__last_name', 'user__first_name', 'user__email')
    list_filter = ('created_on',)
    date_hierarchy = 'created_on'
    list_max_show_all   = 200
    list_per_page       = 200


class TimeSlotAdmin(admin.ModelAdmin):
    """Time slot admin model."""

    model = TimeSlot
    list_display = ('date_time', 'active', 'rank')
    ordering = ('rank', 'date_time')
    list_editable = ['rank']


admin.site.register(Candidate, CandidateAdmin)
admin.site.register(TimeSlot, TimeSlotAdmin)
