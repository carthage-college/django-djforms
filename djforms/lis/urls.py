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
    # generic success view
    url(
        r'^success/',
        TemplateView.as_view(template_name='lis/data_entered.html'),
        name='lis_success'
    )
]
