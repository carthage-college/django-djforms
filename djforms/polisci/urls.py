from django.conf.urls.defaults import *
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djforms.polisci',
    url(r'^$', RedirectView.as_view(url='/political-science/')),
    url(r'^model-united-nations/success/$', TemplateView.as_view(template_name="polisci/mun/registration_done.html")),
    url(r'^model-united-nations/registration/$', 'mun.views.registration_form', name='mun_registration_form'),
)
