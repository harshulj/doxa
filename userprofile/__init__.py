# South rules
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^userprofile\.countries\.CountryField"])

# Signals Caught
from registration.signals import user_activated
from userprofile.models import UserProfile, ProfilePic

def create_userprofile(sender, user, request, **kwargs):
	profile = UserProfile.objects.create(user=user)
	profile_pic = ProfilePic.objects.create(user=user)

user_activated.connect(create_userprofile)
