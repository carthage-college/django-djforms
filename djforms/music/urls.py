from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from djforms.music.ensembles.choral.views import candidate
from djforms.music.ensembles.choral.forms import CandidateForm

urlpatterns = patterns('djforms.music.ensembles.choral.views',
    url(
        r'^ensembles/choral/tryout/success/$',
        TemplateView.as_view(template_name="music/ensembles/choral/tryout_done.html")
    ),
    url(
        r'^ensembles/choral/tryout/manager/$', 'manager',
        name="choral_ensemble_manager"
    ),
    url(
        r'^ensembles/choral/tryout/$', 'candidate',
        name="choral_ensemble_candidate"
    ),
)
