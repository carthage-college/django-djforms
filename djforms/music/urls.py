from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from djforms.music.ensembles.choral.views import candidate
from djforms.music.ensembles.choral.forms import CandidateForm

urlpatterns = patterns('djforms.music',
    # choral tryouts
    url(
        r'^ensembles/choral/tryout/success/$',
        TemplateView.as_view(
            template_name="music/ensembles/choral/done.html"
        ),
        name="choral_tryout_success"
    ),
    url(
        r'^ensembles/choral/tryout/manager/$',
        'ensembles.choral.views.manager',
        name="choral_ensemble_manager"
    ),
    url(
        r'^ensembles/choral/tryout/$',
        'ensembles.choral.views.candidate',
        name="choral_ensemble_candidate"
    ),
    # music theatre summer camp
    url(
        r'^theatre/summer-camp/$',
        'theatre.summer_camp.views.registration',
        name="music_theatre_summer_camp_registration"
    ),
    url(
        r'^theatre/summer-camp/success/$',
        TemplateView.as_view(
            template_name="music/theatre/summer_camp/registration_done.html"
        ),
        name="music_theatre_summer_camp_success"
    ),
)
