from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^success/$', direct_to_template, {'template': 'alumni/data_entered.html'}),
    url(r'^memory/(?P<quid>\d+)/detail/$', 'djforms.alumni.memory.views.questionnaire_detail', name="memory_questionnaire_detail"),
    url(r'^memory/$', 'djforms.alumni.memory.views.questionnaire_form', name='memory_questionnaire_form'),
    # homecoming attendance
    url(r'^homecoming/success/$', direct_to_template, {'template': 'alumni/homecoming/attendance_done.html'}),
    url(r'^homecoming/attendees/(?P<year>\d+)/$', 'djforms.alumni.homecoming.views.attendees', name="homecoming_attendees_year"),
    url(r'^homecoming/attendees/$', 'djforms.alumni.homecoming.views.attendees', name="homecoming_attendees"),
    url(r'^homecoming/$', 'djforms.alumni.homecoming.views.attendance', name='homecoming_attendance'),
    # classnotes
    url(r'^classnotes/success/$', direct_to_template, {'template': 'alumni/classnotes/done.html'}),
    url(r'^classnotes/archives/(?P<year>\d+)/$', 'djforms.alumni.classnotes.views.archives', name="classnotes_archives_year"),
    url(r'^classnotes/carthaginian/$', 'djforms.alumni.classnotes.views.screenscrape', name="classnotes_archives_year"),
    url(r'^classnotes/archives/$', 'djforms.alumni.classnotes.views.archives', name="classnotes_archives"),
    url(r'^classnotes/$', 'djforms.alumni.classnotes.views.contact', name='classnotes_form'),
    # alumni directory
    url(r'^directory/$', direct_to_template, {'template': 'alumni/directory/home.html'}),
    # mws reunion
    url(r'^msw/reunion/success/$', direct_to_template, {'template': 'alumni/msw/reunion_contact_done.html'}),
    url(r'^msw/reunion/archives/$', 'djforms.alumni.msw.views.reunion_contact_archives', name="reunion_contact_archives"),
    url(r'^msw/reunion/(?P<cid>\d+)/detail/$', 'djforms.alumni.msw.views.reunion_contact_detail', name="reunion_contact_detail"),
    url(r'^msw/reunion/$', 'djforms.alumni.msw.views.reunion_contact_form', name='reunion_contact_form'),
    # distinguised alumni nomination
    url(r'^distinguished/nomination/success/$', direct_to_template, {'template': 'alumni/data_entered.html'}),
    url(r'^distinguished/nomination/$', 'djforms.alumni.distinguished.views.nomination_form', name='nomination_form'),
)
