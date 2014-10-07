from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.lis',
    # print requests
    url(
        r'^print-request/$',
        'printjobs.views.print_request'
    ),
    # generic success view
    url(
        r'^success/',
        TemplateView.as_view(template_name='lis/data_entered.html'),
        name="lis_success"
    ),
    # course-ference
    url(
        r'^conferences/course-ference/map/json/$',
        'conferences.course_ference.views.json_map_data',
        name='course_ference_json_map_data'
    ),
    url(
        r'^conferences/course-ference/map/$',
        TemplateView.as_view(
            template_name='lis/conferences/course_ference/map.html'
        )
    ),
    url(
        r'^conferences/course-ference/(?P<reg_type>[\d\w]+)/success/$',
        'conferences.course_ference.views.registration_success',
        name="course_ference_registration_success"
    ),
    url(
        r'^conferences/course-ference/(?P<reg_type>[\d\w]+)/$',
        'conferences.course_ference.views.registration_form',
        name='course_ference_registration_form'
    ),
)
