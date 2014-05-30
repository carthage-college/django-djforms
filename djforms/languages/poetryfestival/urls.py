from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.languages.poetryfestival.views',
    url(
        r'^$', 'signup_form', name='signup_form'
    ),
    url(
        r'^success/',
        TemplateView.as_view(template_name="languages/poetryfestival/data_entered.html"),
        name="poetry_festival_success"
    ),
)
