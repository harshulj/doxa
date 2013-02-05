from django.contrib import admin
from userprofile.models import UserProfile, ProfilePic

class UserProfileAdmin(admin.ModelAdmin):
	pass

class ProfilePicAdmin(admin.ModelAdmin):
	pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ProfilePic, ProfilePicAdmin)
