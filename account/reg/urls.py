from django.conf.urls.defaults import *

from doxa import settings 

from account.reg.forms import UserRegistrationForm
from account.reg.views import register, login

urlpatterns = patterns('',
	url(r'^accounts/login/$', login, {'template': 'registration/login.html'}, name='auth_login'),
	url(r'^accounts/register/$', register, name='registration_register'),
	url(r'^accounts/', include('account.reg.backends.doxa.urls')),
)
