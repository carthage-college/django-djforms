from django.conf.urls.defaults import *
from mysite.polls.models import Poll
from mysite.contact_form.views import contact_form

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^polls/', include('mysite.polls.urls')),
    (r'^contact/', include('mysite.contact_form.urls')),
    (r'^admin/', include(admin.site.urls)),
)
