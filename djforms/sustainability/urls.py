from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.sustainability.green.views',
    url(
        r'^green/pledge/success/$',
        TemplateView.as_view(
            template_name="sustainability/green/done.html"
        ),
        name="green_pledge_success"
    ),
    url(
        r'^green/pledge/archives/$',
        'pledge_archives', name="green_pledge_archives"
    ),
    url(
        r'^green/pledge/$',
        'pledge_form', name="green_pledge_form"
    )
)
