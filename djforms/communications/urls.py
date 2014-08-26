from django.conf.urls.defaults import *
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djforms.communications.printrequest.views',
    url(
        r'^printrequest/$', TemplateView.as_view(
            template_name='communications/print/form.html'
        ),
        name='home'
    ),
    url(
        r'^printrequest/success/$', TemplateView.as_view(
            template_name='communications/print/form_success.html'
        ),
        name='success'
    ),
    url(
        r'^print-request/$',
        'form',
        name='print_request_form'
    ),
)
