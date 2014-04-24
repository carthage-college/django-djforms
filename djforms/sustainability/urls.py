from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(
        r'^green/pledge/success/$',
        TemplateView.as_view(
            template_name="sustainability/green/pledge_done.html"
        ),
        name="pledge_form_success"
    ),
    url(
        r'^green/pledge/archives',
        'djforms.sustainability.green.views.pledge_archives',
        name="pledge_archives"
    ),
    url(
        r'^green/pledge/$',
        'djforms.sustainability.green.views.pledge_form',
        name="pledge_form"
    ),
)
