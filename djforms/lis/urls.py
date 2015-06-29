from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.lis',
    # print requests
    url(
        r'^print-request/$',
        'printjobs.views.print_request'
    ),
    # generic success view
    url(
        r'^success/',
        TemplateView.as_view(template_name='lis/data_entered.html'),
        name="lis_success"
    ),
)
