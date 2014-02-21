from django.conf.urls.defaults import *
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/videos/')),
    url(r'^success/$', TemplateView.as_view(template_name="video/contest_done.html")),
    url(r'^entry/$', 'djforms.video.views.contest_form', name='contest_form'),
    url(r'^entry/(?P<tag>.*)/archives', 'djforms.video.views.contest_archives', name='contest_archives'),
)
