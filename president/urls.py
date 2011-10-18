from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^contact/success/$', direct_to_template, {'template': 'president/contact/done.html'}),
    url(r'^contact/$', 'djforms.president.contact.views.contact_form', name="contact_form"),
)
