from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.alumni.classnotes import views as classnotes
from djforms.alumni.distinguished import views as distinguished
from djforms.alumni.memory import views as memory


urlpatterns = [
    url(
        r'^success/$',
        TemplateView.as_view(template_name='alumni/data_entered.html')
    ),
    # classnotes
    url(
        r'^classnotes/carthaginian/$',
        classnotes.screenscrape,
        name='classnotes_carthaginian'
    ),
    url(
        r'^classnotes/success/$',
        TemplateView.as_view(template_name='alumni/classnotes/done.html'),
        name='classnotes_success'
    ),
    url(
        r'^classnotes/archives/(?P<year>\d+)/',
        classnotes.archives,
        name='classnotes_archives_year'
    ),
    url(
        r'^classnotes/archives/$',
        classnotes.archives,
        name='classnotes_archives'
    ),
    url(
        r'^classnotes/inmemoriam/$',
        classnotes.obits,
        name='classnotes_obits'
    ),
    url(
        r'^classnotes/$',
        classnotes.contact,
        name='classnotes_form'
    ),
    # distinguised alumni nomination
    url(
        r'^distinguished/nomination/success/$',
        TemplateView.as_view(template_name='alumni/data_entered.html'),
        name='distinguished_nomination_success'
    ),
    url(
        r'^distinguished/nomination/',
        distinguished.nomination_form,
        name='distinguished_nomination_form'
    ),
    # fond memories
    url(
        r'^memory/success/$',
        TemplateView.as_view(
            template_name='alumni/memory/done.html'
        ),
        name='memory_questionnaire_success'
    ),
    url(
        r'^memory/archives/$',
        memory.questionnaire_archives,
        name='memory_questionnaire_archives'
    ),
    url(
        r'^memory/(?P<quid>\d+)/detail/$',
        memory.questionnaire_detail,
        name='memory_questionnaire_detail'
    ),
    url(
        r'^memory/(?P<campaign>[a-zA-Z0-9_-]+)',
        memory.questionnaire_form,
        name='memory_questionnaire_promo_form'
    ),
    url(
        r'^memory',
        memory.questionnaire_form,
        name='memory_questionnaire_form'
    )
]
