# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe
from djforms.processors.models import *


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display  = (
        'last_name',
        'contact_name',
        'email',
        'comments',
        'operator',
        'promotion',
        'time_stamp',
        'status',
        'auth',
        'cycle',
        'payments',
        'total',
        'start_date',
        'transid',
    )
    ordering = (
        '-id',
        'promotion',
        '-time_stamp',
        'status',
        'auth',
        'avs',
        'cycle',
        'payments',
        'start_date',
    )
    list_filter = ('status', 'promotion')
    search_fields = ('transid', 'cc_4_digits', 'cc_name')
    list_max_show_all = 500
    list_per_page = 500

    def contact_name(self, obj):
        return mark_safe(
            '<strong><a href="{0}{1}/">{2}</a></strong>'.format(
                '/forms/admin/processors/contact/',
                obj.cid(),
                obj.first_name(),
            ),
        )
    contact_name.allow_tags = True
    contact_name.short_description = 'First name (contact info)'


    def invoice_url(self, obj):
        return mark_safe('<a href="{0}">{1}</a>'.format(obj.firm_url, obj.firm_url))
    invoice_url.allow_tags = True
    invoice_url.short_description = 'Invoice'


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display  = (
        'last_name',
        'first_name',
        'email',
        'phone',
        'address1',
        'address2',
        'city',
        'state',
        'postal_code',
    )
    ordering = ('-id', 'last_name', 'city', 'state', 'postal_code')
    list_filter = ('state',)
    search_fields = ('last_name', 'phone', 'city', 'state', 'postal_code')
    raw_id_fields = ("order",)


admin.site.register(Order, OrderAdmin)
admin.site.register(Contact, ContactAdmin)
