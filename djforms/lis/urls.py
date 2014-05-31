from django.conf.urls.defaults import *
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.lis',
    # For room and equipment reserve environment
    url(
        r'^secure/reference/articles',
        TemplateView.as_view(
            template_name='lis/secure/reference/articles.html'
        )
    ),
    url(
        r'^equipment-reserve/$',
        'equipmentform.views.equipment_reserve'
    ),
    url(
        r'^print-request/$',
        'printjobs.views.print_request'
    ),
    url(
        r'^success',
        TemplateView.as_view(template_name='lis/data_entered.html'),
        name="lis_success"
    ),
    # e-looking glass conference registration
    url(
        r'^conferences/looking-glass/success/$',
        TemplateView.as_view(
            template_name='lis/conferences/looking_glass/done.html'
        ),
        name="looking_glass_registration_success"
    ),
    url(
        r'^conferences/looking-glass/$',
        'conferences.looking_glass.views.registration_form',
        name='looking_glass_registration_form'
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
