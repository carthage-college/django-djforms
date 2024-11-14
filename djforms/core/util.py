# -*- coding: utf-8 -*-

import csv

from django.apps import apps
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.template.defaultfilters import slugify


def export_as_csv_action(description='Export selected objects as CSV file',
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        #field_names = set([field.name for field in opts.fields])
        field_names = [field.name for field in opts.fields]
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse('', content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename={0}.csv'.format(
            opts.replace('.', '_'),
        )

        writer = csv.writer(response)
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field, None) for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv


def export(qs, fields=None):
    model = qs.model
    response = HttpResponse('', content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename={0}.csv'.format(
        slugify(model.__name__),
    )
    writer = csv.writer(response)
    # Write headers to CSV file
    if fields:
        headers = fields
    else:
        headers = []
        for field in model._meta.fields:
            headers.append(field.name)

        for field in model._meta.many_to_many:
            headers.append(field.name)

    writer.writerow(headers)
    # Write data to CSV file
    for obj in qs:
        row = []
        for field in headers:
            if field in headers:
                val = getattr(obj, field)
                try:
                    generic_choices = '['
                    for v in val.all():
                        generic_choices += v.name + ', '
                    generic_choices += ']'
                    row.append(generic_choices)
                except:
                    if callable(val):
                        val = val()
                    row.append(val)
        writer.writerow(row)

    # Return CSV file to browser as download
    return response


def admin_list_export(request, app_label, model_name, queryset=None, fields=None, list_display=True):
    if not request.user.is_staff:
        return HttpResponseForbidden()
    if not queryset:
        model = apps.get_model(app_label, model_name)
        queryset = model.objects.all()
        filters = dict()
        for key, value in request.GET.items():
            if key not in ('ot', 'o', 'p'):
                filters[str(key)] = str(value)
        if len(filters):
            queryset = queryset.filter(**filters)

    return export(queryset, fields)
