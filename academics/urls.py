from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('djforms.academics',
    url(r'^faculty/teaching/success/$', direct_to_template, {'template': 'academics/faculty/distinguished_teaching_award_done.html'}),
    url(r'^faculty/teaching/award/$', 'faculty.views.distinguished_teaching_award', name='distinguished_teaching_award'),
)
