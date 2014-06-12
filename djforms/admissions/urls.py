from django.conf.urls.defaults import *
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djforms.admissions',
    #url(
    #    r'^$', RedirectView.as_view(url='/admissions/visit/')
    #),
    url(
        r'^visit/success/$',
        TemplateView.as_view(template_name='admissions/visitday/success.html'),
        name="visitday_success"
    ),
    url(
        r'^visit/$',
        TemplateView.as_view(template_name='admissions/visitday/home.html'),
        name="visitday_home"
    ),
    url(
        r'^visit/(?P<event_type>[a-zA-Z0-9_-]+)/$',
        'visitdays.views.VisitDayForm',
        name='visitday_form'
    ),
    url(
        r'^admitted/success/$',
        TemplateView.as_view(template_name='admissions/admitted/success.html'),
        name="admitted_success"
    ),
    url(
        r'^admitted/$',
        'admitted.views.chance_of_form',
        name='chance_of_form'
    ),
    url(
        r'^china/success/$',
        TemplateView.as_view(template_name='admissions/china/success.html'),
        name="admissions_china_success"
    ),
    url(
        r'^china/$', 'china.views.interest_form', name='interest_form'
    ),
)
