import csv

from django.http import HttpResponse, HttpResponseForbidden
from django.template.defaultfilters import slugify
from django.db.models.loading import get_model

def export(qs, fields=None):
    model = qs.model
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % slugify(model.__name__)
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
        model = get_model(app_label, model_name)
        queryset = model.objects.all()
        filters = dict()
        for key, value in request.GET.items():
            #if key not in ('ot', 'o'):
            if key not in ('ot', 'o', 'p'):
                filters[str(key)] = str(value)
        if len(filters):
            queryset = queryset.filter(**filters)

    return export(queryset, fields)
    """
    Create your own change_list.html for your admin view and put something like this in it:
    {% block object-tools %}
    <ul class="object-tools">
        <li><a href="csv/{% for key, value in cl.params.items %}{% if forloop.first %}?{% else %}&{% endif %}{{ key }}={{ value }}{% endfor %}" class="addlink">Export to CSV</a></li>
    {% if has_add_permission %}
        <li><a href="add/{% if is_popup %}?_popup=1{% endif %}" class="addlink">{% blocktrans with cl.opts.verbose_name|escape as name %}Add {{ name }}{% endblocktrans %}</a></li>
    {% endif %}
    </ul>
    {% endblock %}
    """

