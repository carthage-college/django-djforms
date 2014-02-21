from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.academics',
    url(
        r'^faculty/teaching/success/$',
        TemplateView.as_view(
            template_name="academics/faculty/distinguished_teaching_award_done.html"
        )
    ),
    url(
        r'^faculty/teaching/award/$',
        'faculty.views.distinguished_teaching_award', name='distinguished_teaching_award'
    ),
)
