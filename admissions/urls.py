from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^$', redirect_to, {'url': '/admissions/visit/', 'permanent': True}),
    url(r'^success/$', TemplateView.as_view(template_name='admissions/data_entered.html')),
    url(r'^visit/(?P<event_type>[a-zA-Z0-9_-]+)/$', 'djforms.admissions.visitdays.views.VisitDayForm', name='visit_day_form'),
    url(r'^admitted/success/$', TemplateView.as_view(template_name='admissions/admitted/success.html')),
    url(r'^admitted/$', 'djforms.admissions.admitted.views.chance_of_form', name='chance_of_form'),
)
