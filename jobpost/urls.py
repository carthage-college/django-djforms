from django.conf.urls.defaults import *

urlpatterns = patterns('djforms.jobpost.views',
  url(r'^data_entered/$',
      view    = 'data_entered',
      name    = 'data_entered',
  ),
  url(r'^createpost/$',
      view    = 'post_create',
      name    = 'post_create',
  ),
  url(r'^departments/(?P<slug>[-\w]+)/$',
      view    = 'department_detail',
      name    = 'department_detail',
  ),
  url(r'^departments/page/(?P<page>\w)/$',
      view    = 'department_list',
      name    = 'department_list_paginated',
  ),
  url(r'^departments/$',
      view    = 'department_list',
      name    = 'department_list',
  ),
  url(r'^search/$',
      view    = 'search',
      name    = 'post_search',
  ),
  url(r'^page/(?P<page>\w)/$',
      view    = 'post_list',
      name    = 'post_index_paginated',
  ),
  url(r'^$',
      view    = 'post_list',
      name    = 'post_index',
  ),
    url(r'^(?P<slug>[-\w]+)/$',
      view    = 'post_detail',
      name    = 'post_detail',
  ),
)
