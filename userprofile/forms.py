from django import forms
from userprofile.models import UserProfile, ProfilePic

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		exclude = ('user',)

class ProfilePicForm(forms.ModelForm):
	class Meta:
		model = ProfilePic
		exclude = ('user', 'valid')
