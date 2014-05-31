from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.biology',
    url(
        r'^genomics/phage-hunters/success/$',
        TemplateView.as_view(
            template_name="biology/genomics/phage_hunter_done.html"
        ),
        name="phage_hunters_success"
    ),
    url(
        r'^genomics/phage-hunters/archives/$',
        'genomics.views.phage_hunter_archives',
        name="phage_hunters_archives"
    ),
    url(
        r'^genomics/phage-hunters/application/$',
        'genomics.views.phage_hunter_form',
        name='phage_hunters_form'
    ),
    url(
        r'^genomics/phage-hunters/(?P<pid>\d+)/detail/$',
        'genomics.views.phage_hunter_detail',
        name="phage_hunters_detail"
    ),
)
