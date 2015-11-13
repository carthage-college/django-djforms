from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.scholars.views',
    # archives
    url(
        r'^archives/(?P<ptype>[-\w]+)/(?P<medium>[-\w]+)/(?P<year>\d{4})/$',
        'presentation.archives', name="presentation_archives"
    ),
    url(
        r'^archives/(?P<ptype>[-\w]+)/(?P<medium>[-\w]+)/$',
        'presentation.archives',name="presentation_archives_home"
    ),
    # print
    url(
        r'^presentation/print/','print.alpha'
    ),
    url(
        r'^presentation/alpha/','print.alpha',
        {'template':'scholars/print/alpha.html'}
    ),
    # presentation crud
    url(
        r'^presentation/success/$',
        TemplateView.as_view(template_name='scholars/presentation/done.html'),
        name="presentation_form_done"
    ),
    url(
        r'^presentation/manager/$',
        'presentation.manager', name="presentation_manager"
    ),
    url(
        r'^presentation/action/$',
        'presentation.action', name="presentation_action"
    ),
    url(
        r'^presentation/(?P<pid>\d+)/update/$',
        'presentation.form',name="presentation_update"
    ),
    url(
        r'^presentation/(?P<pid>\d+)/detail/$',
        'presentation.detail',name="presentation_detail"
    ),
    url(
        r'^presentation/$',
        'presentation.form',name="presentation_form"
    ),
    # send email to all presentation leaders
    # 10 Apr 2014: currently not completed but needed for 2015
    #url(
    #    r'^presenters/email/leaders/$',
    #    'presentation.email_leaders',name="email_leaders"
    #),
    # send email to a presentation's leader and sponsor
    url(
        r'^presenters/email/success/$',
        TemplateView.as_view(
            template_name='scholars/presenters/email_done.html'
        ),
        name="email_presenters_done"
    ),
    url(
        r'^presenters/email/all/$',
        'presentation.email_all_presenters',name="email_all_presenters"
    ),
    url(
        r'^presenters/email/(?P<pid>\d+)/(?P<action>[-\w]+)/$',
        'presentation.email_presenters',name="email_presenters"
    ),
)
