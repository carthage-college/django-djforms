from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from djforms.music.ensembles.choral.views import candidate
from djforms.music.ensembles.choral.forms import CandidateForm

urlpatterns = patterns('djforms.music.ensembles.choral.views',
    url(r'^ensembles/choral/tryout/success/$', direct_to_template, {'template': 'music/ensembles/choral/tryout_done.html'}),
    url(r'^ensembles/choral/tryout/$', 'candidate', name="choral_ensemble_candidate"),
)
