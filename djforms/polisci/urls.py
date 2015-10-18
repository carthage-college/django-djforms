from django.conf.urls.defaults import *
from django.views.generic import TemplateView, RedirectView

urlpatterns = patterns('djforms.polisci',
    url(
        r'^$', RedirectView.as_view(url='/political-science/')
    ),
    url(
        r'^model-united-nations/success/$',
        TemplateView.as_view(
            template_name="polisci/mun/done.html"
        ),
        name="model_united_nations_success"
    ),
    url(
        r'^model-united-nations/registration/$',
        'mun.views.registration',
        name='model_united_nations_registration'
    ),
    # had to revert to old reg form
    #url(
    #    r'^model-united-nations/success/$',
    #    TemplateView.as_view(
    #        template_name="polisci/model_united_nations/done.html"
    #    ),
    #    name="model_united_nations_success"
    #),
    #url(
    #    r'^model-united-nations/registration/$',
    #    'model_united_nations.views.registration',
    #    name='model_united_nations_registration'
    #),
    url(
        r'^iea/proposal/success/$',
        TemplateView.as_view(
            template_name="polisci/iea/proposal/done.html"
        ),
        name="iea_proposal_success"
    ),
    url(
        r'^iea/proposal/$',
        'iea.proposal.views.form',
        name='iea_proposal'
    ),
    url(
        r'^iea/registration/success/$',
        TemplateView.as_view(
            template_name="polisci/iea/registration/done.html"
        ),
        name="iea_registration_success"
    ),
    url(
        r'^iea/registration/$',
        'iea.registration.views.form',
        name='iea_registration'
    ),
)
