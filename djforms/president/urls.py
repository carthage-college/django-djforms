from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.president',
    # honorary degree nomination
    url(
        r'^honorary-degree/nomination/success/$',
        TemplateView.as_view(
            template_name='president/honorary_degree/done.html'
        ),
        name="honorary_degree_nomination_success"
    ),
    url(
        r'^honorary-degree/nomination/$',
        'honorary_degree.views.nomination_form',
        name='honorary_degree_nomination_form'
    )
)
