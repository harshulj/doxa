from django.utils.timezone import now
from haystack import site
from haystack.indexes import *
from userprofile.models import UserProfile

class UserProfileIndex(RealTimeSearchIndex):
	text = CharField(document=True, use_template=True)
	user = CharField(model_attr='user')

	def index_queryset(self):
		return UserProfile.objects.filter()

site.register(UserProfile, UserProfileIndex)
