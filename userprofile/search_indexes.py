from django.utils.timezone import now
from haystack import site
from haystack.indexes import *
from userprofile.models import UserProfile

class UserProfileIndex(SearchIndex):
	text = CharField(document=True, use_template=True)
	user = CharField(model_attr='user')
	
	def prepare_user(self, obj):
		return "%s" % (obj.name)

	def index_queryset(self):
		return UserProfile.objects.filter()

site.register(UserProfile, UserProfileIndex)
