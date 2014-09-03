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
        r'^wipcs/proposal/success/$',
        TemplateView.as_view(
            template_name="polisci/wipcs/proposal/done.html"
        ),
        name="wipcs_proposal_success"
    ),
    url(
        r'^wipcs/proposal/$',
        'wipcs.proposal.views.form',
        name='wipcs_proposal'
    ),
    url(
        r'^wipcs/registration/success/$',
        TemplateView.as_view(
            template_name="polisci/wipcs/registration/done.html"
        ),
        name="wipcs_registration_success"
    ),
    url(
        r'^wipcs/registration/$',
        'wipcs.registration.views.form',
        name='wipcs_registration'
    ),
)
