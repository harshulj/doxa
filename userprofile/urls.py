from django.conf.urls.defaults import *
from userprofile.views import my_profile, edit_profile, user_profile

urlpatterns = patterns('',
	url(r'^profile/$', my_profile, name='userprofile_my_profile'),
	url(r'^profile/edit/$', edit_profile, name='userprofile_edit_profile'),
	url(r'^user/(?P<username>[\w.@+-]+)/$', user_profile, name='userprofile_user_profile'),
)
