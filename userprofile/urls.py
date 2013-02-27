from django.conf.urls.defaults import *
from userprofile.views import  edit_profile, user_profile

urlpatterns = patterns('',
	url(r'^edit/$', edit_profile, name='userprofile_edit_profile'),
	url(r'^(?P<username>[\w.@+-]+)/$', user_profile, name='userprofile_user_profile'),
)
