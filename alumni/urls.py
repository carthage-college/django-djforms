from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.alumni.memory.views',
    url(r'^success/$', direct_to_template, {'template': 'alumni/data_entered.html'}),
    url(r'^memory/(?P<quid>\d+)/detail/$', 'questionnaire_detail', name="memory_questionnaire_detail"),
    url(r'^memory/$', 'questionnaire_form', name='memory_questionnaire_form'),
)
