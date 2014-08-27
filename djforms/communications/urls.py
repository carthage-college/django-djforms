from django.conf.urls.defaults import *
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djforms.communications.printrequest.views',
    url(
        r'^print-request/success/$', TemplateView.as_view(
            template_name='communications/printrequest/form_success.html'
        ),
        name='success'
    ),
    url(
        r'^print-request/$',
        'print_request',
        name='print_request'
    ),
)
