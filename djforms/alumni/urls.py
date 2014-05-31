from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.alumni',
    url(
        r'^success/$',
        TemplateView.as_view(template_name='alumni/data_entered.html')
    ),
    # homecoming attendance
    url(
        r'^homecoming/success/$',
        TemplateView.as_view(
            template_name='alumni/homecoming/attendance_done.html'
        ),
        name="homecoming_attendance_success"
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
    # alumni directory UI maquette
    #url(r'^directory/$', TemplateView.as_view(template_name='alumni/directory/home.html')),
    # distinguised alumni nomination
    url(
        r'^distinguished/nomination/success/$',
        TemplateView.as_view(template_name='alumni/data_entered.html'),
        name="distinguished_nomination_success"
    ),
    url(
        r'^distinguished/nomination/$',
        'distinguished.views.nomination_form',
        name='distinguished_nomination_form'
    )
)
