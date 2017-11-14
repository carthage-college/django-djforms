from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.admissions.visitdays import views as visitdays
from djforms.admissions.admitted import views as admitted


urlpatterns = [
    url(
        r'^visit/success/$',
        TemplateView.as_view(template_name='admissions/visitday/success.html'),
        name='visitday_success'
    ),
    url(
        r'^visit/$',
        TemplateView.as_view(template_name='admissions/visitday/home.html'),
        name='visitday_home'
    ),
    url(
        r'^visit/(?P<event_type>[a-zA-Z0-9_-]+)/$',
        visitdays.visit_day_form,
        name='visitday_form'
    ),
    url(
        r'^admitted/success/$',
        TemplateView.as_view(template_name='admissions/admitted/success.html'),
        name='admitted_success'
    ),
    url(
        r'^admitted/$',
        admitted.chance_of_form,
        name='chance_of_form'
    )
]
