from django.conf.urls.defaults import *

urlpatterns = patterns('',
	url(r'', include('actstream.urls')),
)
