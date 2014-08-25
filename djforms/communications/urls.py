from django.conf.urls.defaults import *
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djforms.communications',
                       
    url(r'^test/', TemplateView.as_view(template_name='communications/print/form.html', name='home')                       
                                           
)