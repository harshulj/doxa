# Custom register and activate views for django-registration.
# Used for redirecting user to home if they are already loggedin.
from django.http import HttpResponseRedirect
from  django.contrib.auth import views as auth_views

from doxa import settings
from .forms import UserRegistrationForm

if getattr(settings, 'INVITE_MODE', False):
	from invitation.views import register as registration_register
	backend = 'invitation.backends.InvitationBackend'
else:
	from registration.views import register as registration_register
	backend = 'account.reg.backends.doxa.DoxaBackend'

def register(request, success_url=None,form_class=UserRegistrationForm, profile_callback=None,template_name='registration/registration_form.html',extra_context=None):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return registration_register(request, backend, success_url, form_class, profile_callback,  extra_context)

def login(request, template='registration/login.html', extra_context=None):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		return auth_views.login(request,template)
