from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('djforms.lis',
    # copy/print card request
    url(
        r'^copy-print/$',
        'copyprint.views.index'
    ),
    # print requests
    url(
        r'^print-request/$',
        'printjobs.views.index'
    ),
    # generic success view
    url(
        r'^success/',
        TemplateView.as_view(template_name='lis/data_entered.html'),
        name="lis_success"
    ),
    # mathematica
    url(
        r'^conferences/mathematica/registration/success/$',
        'conferences.mathematica.views.registration_success',
        name="mathematica_registration_success"
    ),
    url(
        r'^conferences/mathematica/registration/$',
        'conferences.mathematica.views.registration_form',
        name='mathematica_registration_form'
    ),
)
