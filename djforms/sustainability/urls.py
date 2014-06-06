from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(
        r'^green/pledge/success/$',
        TemplateView.as_view(
            template_name="sustainability/green/done.html"
        ),
        name="green_pledge_success"
    ),
    url(
        r'^green/pledge/archives/$',
        'djforms.sustainability.green.views.pledge_archives',
        name="green_pledge_archives"
    ),
    url(
        r'^green/pledge/$',
        'djforms.sustainability.green.views.pledge_form',
        name="green_pledge_form"
    ),
)
