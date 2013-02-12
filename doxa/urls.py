from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

from doxa import settings 
from django.contrib import admin
admin.autodiscover()


from account.reg.forms import UserRegistrationForm
from invitation.views import register

# Change URLs given the INVITE_MODE setting, useful for tests
if getattr(settings, 'INVITE_MODE', False):
    urlpatterns = patterns('',
        url(r'^accounts/register/$',    register,
                                            {
                                                'form_class': UserRegistrationForm,
                                                'backend': 'invitation.backends.InvitationBackend',
                                            },
                                            name='registration_register'),
    )
else:
    urlpatterns = patterns('',
        url(r'^accounts/register/$',    register,
                                            {
                                                'form_class': UserRegistrationForm,
                                                'backend': 'account.reg.backends.doxa.DoxaBackend',
                                            },
                                            name='registration_register'),
    )

urlpatterns += patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('account.reg.backends.doxa.urls')),
    url(r'^accounts/', include('invitation.urls')),
    url(r'', include('userprofile.urls')),
    url(r'^polls/', include('polls_and_opinions.urls.polls')),
    url(r'^$', direct_to_template, { 'template': 'index.html'} ),
    url(r'^invite/', include('privatebeta.urls')),
    url(r'^search/', include('haystack.urls')),
    url(r'accounts/', include('social_auth.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)
if settings.DEBUG:
    urlpatterns += patterns('', (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))
