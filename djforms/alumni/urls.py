from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.alumni',
    url(
        r'^success/$',
        TemplateView.as_view(template_name='alumni/data_entered.html')
    ),
    # classnotes
    url(
        r'^classnotes/carthaginian/$',
        'classnotes.views.screenscrape',
        name="classnotes_carthaginian"
    ),
    url(
        r'^classnotes/success/$',
        TemplateView.as_view(template_name='alumni/classnotes/done.html'),
        name="classnotes_success"
    ),
    url(
        r'^classnotes/archives/(?P<year>\d+)/',
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
    url(
        r'^directory/$',
        TemplateView.as_view(template_name='alumni/directory/home.html')
    ),
    # distinguised alumni nomination
    url(
        r'^distinguished/nomination/success/$',
        TemplateView.as_view(template_name='alumni/data_entered.html'),
        name="distinguished_nomination_success"
    ),
    url(
        r'^distinguished/nomination/',
        'distinguished.views.nomination_form',
        name='distinguished_nomination_form'
    ),
    # fond memories
    url(
        r'^memory/success/$',
        TemplateView.as_view(
            template_name='alumni/memory/done.html'
        ),
        name="memory_questionnaire_success"
    ),
    url(
        r'^memory/archives/$',
        'memory.views.questionnaire_archives',
        name="memory_questionnaire_archives"
    ),
    url(
        r'^memory/(?P<quid>\d+)/detail/$',
        'memory.views.questionnaire_detail',
        name="memory_questionnaire_detail"
    ),
    url(
        r'^memory/(?P<campaign>[a-zA-Z0-9_-]+)',
        'memory.views.questionnaire_form',
        name='memory_questionnaire_promo_form'
    ),
    url(
        r'^memory',
        'memory.views.questionnaire_form',
        name='memory_questionnaire_form'
    ),
)
