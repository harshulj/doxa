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
    # Examples:
    # url(r'^$', 'doxa.views.home', name='home'),
    # url(r'^doxa/', include('doxa.foo.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('account.reg.backends.doxa.urls')),
    (r'^accounts/', include('invitation.urls')),
    url(r'^$', direct_to_template, { 'template': 'index.html'} ),
    url(r'^invite/', include('privatebeta.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),)
