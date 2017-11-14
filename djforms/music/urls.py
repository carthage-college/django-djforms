from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.music.ensembles.choral.views import candidate
from djforms.music.ensembles.choral.forms import CandidateForm
from djforms.music.ensembles.choral import views as choral
from djforms.music.theatre.summer_camp import views as summer_camp


urlpatterns = [
    # choral tryouts
    url(
        r'^ensembles/choral/tryout/success/$',
        TemplateView.as_view(
            template_name='music/ensembles/choral/done.html'
        ),
        name='choral_tryout_success'
    ),
    url(
        r'^ensembles/choral/tryout/manager/$',
        choral.manager,
        name='choral_ensemble_manager'
    ),
    url(
        r'^ensembles/choral/tryout/$',
        choral.candidate,
        name='choral_ensemble_candidate'
    ),
    # music theatre summer camp
    url(
        r'^theatre/summer-camp/$',
        summer_camp.registration,
        name='music_theatre_summer_camp_registration'
    ),
    url(
        r'^theatre/summer-camp/success/$',
        TemplateView.as_view(
            template_name='music/theatre/summer_camp/registration_done.html'
        ),
        name='music_theatre_summer_camp_success'
    )
]
