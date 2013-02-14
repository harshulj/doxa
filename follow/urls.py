from django.conf.urls.defaults import *

from relationships.views import relationship_redirect, relationship_list
from follow.views import relationship_handler

urlpatterns = patterns('',
    url(r'^$', relationship_redirect, name='relationship_list_base'),
    url(r'^user/(?P<username>[\w.@+-]+)/(?:(?P<status_slug>[\w-]+)/)?$', relationship_list, name='relationship_list'),
    url(r'^relation/add/(?P<username>[\w.@+-]+)/(?P<status_slug>[\w-]+)/$', relationship_handler, {'add': True}, name='relationship_add'),
    url(r'^relation/remove/(?P<username>[\w.@+-]+)/(?P<status_slug>[\w-]+)/$', relationship_handler, {'add': False}, name='relationship_remove'),
)
