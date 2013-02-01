from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template


from doxa import settings 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'doxa.views.home', name='home'),
    # url(r'^doxa/', include('doxa.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('account.reg.backends.doxa.urls')),
    url(r'^$', direct_to_template, { 'template': 'index.html'} ),
)

if settings.DEBUG:
	urlpatterns += patterns('',(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)
