from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.global_bridge.summer_school.views',
    # summer school
    url(
        r'^summer-school/registration/success/$',
        TemplateView.as_view(
            template_name="summer_school/registration_done.html"
        ),
        name="global_bridge_summer_school_registration_success"
    ),
    url(
        r'^summer-school/registration/$',
        'registration',
        name="global_bridge_summer_school_registration"
    ),
)
