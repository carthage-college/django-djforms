from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.lis.copyprint import views as copyprint
from djforms.lis.printjobs import views as printjobs


urlpatterns = [
    # copy/print card request
    url(
        r'^copy-print/$',
        copyprint.index
    ),
    # print requests
    url(
        r'^print-request/$',
        printjobs.index
    ),
    # print requests success
    url(
        r'^print-request/success/',
        TemplateView.as_view(template_name='lis/printjobs/data_entered.html'),
        name='print_request_success'
    ),
    # generic success view
    url(
        r'^success/',
        TemplateView.as_view(template_name='lis/data_entered.html'),
        name='lis_success'
    )
]
