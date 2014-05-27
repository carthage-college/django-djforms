from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.alumni',
    url(
        r'^success/$',
        TemplateView.as_view(template_name='alumni/data_entered.html')
    ),
    # retired: now a livewhale form
    #url(r'^memory/(?P<quid>\d+)/detail/$', 'memory.views.questionnaire_detail', name="memory_questionnaire_detail"),
    #url(r'^memory/$', 'memory.views.questionnaire_form', name='memory_questionnaire_form'),
    # homecoming attendance
    url(
        r'^homecoming/success/$',
        TemplateView.as_view(
            template_name='alumni/homecoming/attendance_done.html'
        )
    ),
    url(
        r'^homecoming/attendees/(?P<year>\d+)/$',
        'homecoming.views.attendees',
        name="homecoming_attendees_year"
    ),
    url(
        r'^homecoming/attendees/$',
        'homecoming.views.attendees',
        name="homecoming_attendees"
    ),
    url(
        r'^homecoming/$',
        'homecoming.views.attendance',
        name='homecoming_attendance'
    ),
    # classnotes
    url(
        r'^classnotes/carthaginian/$',
        'classnotes.views.screenscrape',
        name="classnotes_archives_year"
    ),
    url(
        r'^classnotes/success/$',
        TemplateView.as_view(template_name='alumni/classnotes/done.html')
    ),
    url(
        r'^classnotes/archives/(?P<year>\d+)/$',
        'classnotes.views.archives',
        name="classnotes_archives_year"
    ),
    url(
        r'^classnotes/archives/$',
        'classnotes.views.archives',
        name="classnotes_archives"
    ),
    url(
        r'^classnotes/inmemoriam/$',
        'classnotes.views.obits',
        name="classnotes_obits"
    ),
    url(
        r'^classnotes/$',
        'classnotes.views.contact',
        name='classnotes_form'
    ),
    # alumni directory
    #url(r'^directory/$', TemplateView.as_view(template_name='alumni/directory/home.html')),
    # mws reunion: RETIRED
    #url(r'^msw/reunion/success/$', TemplateView.as_view(template_name='alumni/msw/reunion_contact_done.html')),
    #url(r'^msw/reunion/archives/$', 'msw.views.reunion_contact_archives', name="reunion_contact_archives"),
    #url(r'^msw/reunion/(?P<cid>\d+)/detail/$', 'msw.views.reunion_contact_detail', name="reunion_contact_detail"),
    #url(r'^msw/reunion/$', 'msw.views.reunion_contact_form', name='reunion_contact_form'),
    # distinguised alumni nomination
    url(
        r'^distinguished/nomination/success/$',
        TemplateView.as_view(template_name='alumni/data_entered.html')
    ),
    url(
        r'^distinguished/nomination/$',
        'distinguished.views.nomination_form',
        name='nomination_form'
    )
)
