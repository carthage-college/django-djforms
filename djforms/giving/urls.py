from django.conf.urls import url
from django.views.generic import TemplateView

from djforms.giving import views


urlpatterns = [
    # list of donors displayed
    url(
        r'^donors/(?P<slug>[a-zA-Z0-9_-]+)',
        views.donors, name='giving_donors_campaign'
    ),
    url(
        r'^donors', views.donors, name='giving_donors'
    ),
    # manager views
    url(
        r'^manager/cash/$',
        views.manager_cash, name='giving_manager_cash'
    ),
    url(
        r'^manager/success',
        TemplateView.as_view(template_name='giving/manager/success.html'),
        name='giving_manager_success'
    ),
    url(
        r'^manager/$',
        views.manager, name='giving_manager_home'
    ),
    url(
        r'^manager/photo/$',
        views.photo_caption, name='photo_caption'
    ),
    url(
        r'^manager/(?P<slug>[a-zA-Z0-9_-]+)/$',
        views.manager, name='giving_manager_home_campaign'
    ),
    # ajax calls for campaign, mini-goal, crowd fund challenge, etc.
    url(
        r'^campaign/(?P<slug>[a-zA-Z0-9_-]+)',
        views.promotion_ajax, name='promotion_ajax'
    ),
    # displayed after form is submitted
    url(
        r'^(?P<transaction>[a-zA-Z0-9_-]+)/(?P<campaign>[a-zA-Z0-9_-]+)/success',
        views.giving_success, name='giving_success_campaign'
    ),
    url(
        r'^(?P<transaction>[a-zA-Z0-9_-]+)/success',
        views.giving_success, name='giving_success_generic'
    ),
    # campaign donation forms
    url(
        r'^(?P<transaction>[a-zA-Z0-9_-]+)/(?P<campaign>[a-zA-Z0-9_-]+)',
        views.giving_form, name='giving_form_campaign'
    ),
    # generic giving
    url(
        r'^(?P<transaction>[a-zA-Z0-9_-]+)',
        views.giving_form, name='giving_form_generic'
    )
]
