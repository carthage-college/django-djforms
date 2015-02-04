from django.conf.urls.defaults import *
from django.views.generic import TemplateView

from djforms.music.ensembles.choral.views import candidate
from djforms.music.ensembles.choral.forms import CandidateForm

urlpatterns = patterns('djforms.music.ensembles.choral.views',
    # choral tryouts
    url(
        r'^ensembles/choral/tryout/success/$',
        TemplateView.as_view(
            template_name="music/ensembles/choral/done.html"
        ),
        name="choral_tryout_success"
    ),
    url(
        r'^ensembles/choral/tryout/manager/$', 'manager',
        name="choral_ensemble_manager"
    ),
    url(
        r'^ensembles/choral/tryout/$', 'candidate',
        name="choral_ensemble_candidate"
    ),
    # music theatre summer camp
    url(
        r'^music/theatre/summer-camp/$', 'registration',
        name="music_theatre_summer_camp"
    ),
    url(
        r'^music/theatre/summer-camp/success/$',
        TemplateView.as_view(
            template_name="music/theatre/summer-camp/registration_done.html"
        ),
        name="music_theatre_summer_camp_success"
    ),
)
