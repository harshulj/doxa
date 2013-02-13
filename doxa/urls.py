from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from doxa import settings 
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('account.reg.urls')),
    url(r'^account/', include('invitation.urls')),
    url(r'', include('userprofile.urls')),
    url(r'^polls/', include('polls_and_opinions.urls.polls')),
    url(r'^$', direct_to_template, { 'template': 'index.html'} ),
    url(r'^invite/', include('privatebeta.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'account/', include('social_auth.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)
if settings.DEBUG:
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
