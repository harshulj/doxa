from django.conf.urls.defaults import *
from userprofile.views import my_profile, edit_profile

urlpatterns = patterns('',
	url(r'^$', my_profile, name='userprofile_my_profile'),
	url(r'^edit/$', edit_profile, name='userprofile_edit_profile'),
)
