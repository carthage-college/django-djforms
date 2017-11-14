from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.sustainability.green import views as green


urlpatterns = [
    url(
        r'^green/pledge/success/$',
        TemplateView.as_view(
            template_name='sustainability/green/done.html'
        ),
        name='green_pledge_success'
    ),
    url(
        r'^green/pledge/archives/$',
        green.pledge_archives, name='green_pledge_archives'
    ),
    url(
        r'^green/pledge/$',
        green.pledge_form, name='green_pledge_form'
    )
]
