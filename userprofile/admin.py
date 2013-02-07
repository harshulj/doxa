from django.contrib import admin
from userprofile.models import UserProfile, ProfilePic

class UserProfileAdmin(admin.ModelAdmin):
	search_fields = ['about', 'short_bio', 'user__username', 'user__first_name', 'user__last_name']
	list_filter = ['dob', 'gender', 'country']
	list_display = ['__unicode__', 'user', 'dob', 'country', 'gender']

class ProfilePicAdmin(admin.ModelAdmin):
	search_fields = ['user__username', 'user__first_name', 'user__last_name']
	list_filter = ['valid']
	list_display = ['image','user', 'valid']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ProfilePic, ProfilePicAdmin)
