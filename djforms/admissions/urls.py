from django.conf.urls.defaults import *
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djforms.admissions',
    url(r'^$', RedirectView.as_view(url='/admissions/visit/')),
    url(r'^success/$', TemplateView.as_view(template_name='admissions/data_entered.html')),
    url(r'^visit/(?P<event_type>[a-zA-Z0-9_-]+)/$', 'visitdays.views.VisitDayForm', name='visit_day_form'),
    url(r'^admitted/success/$', TemplateView.as_view(template_name='admissions/admitted/success.html')),
    url(r'^admitted/$', 'admitted.views.chance_of_form', name='chance_of_form'),
    url(r'^china/success/$', TemplateView.as_view(template_name='admissions/china/success.html')),
    url(r'^china/$', 'china.views.interest_form', name='interest_form'),
)
