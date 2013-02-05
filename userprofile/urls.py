from django.conf.urls.defaults import *
from userprofile.views import my_profile

urlpatterns = patterns('',
	url(r'$', my_profile, name='userprofile_my_profile'),
)
