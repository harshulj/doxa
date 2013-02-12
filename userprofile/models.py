from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from easy_thumbnails.fields import ThumbnailerImageField
from userprofile.countries import CountryField

GENDER_CHOICES = ( ('F', _('Female')), ('M', _('Male')),)

APP_NAME = "userprofile"

class UserProfile(models.Model):
	"""
		This is a user profile model.
	"""
	user = models.OneToOneField(User, related_name="profile")
	short_bio = models.CharField(max_length=100, null=True, blank=True)
	dob = models.DateField(null=True, blank=True)
	country = CountryField(null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
	url = models.URLField(max_length=70, null=True, blank=True)
	about = models.TextField(max_length=200, null=True, blank=True)

	@property
	def name(self):
		return _("%s %s") %( self.user.first_name, self.user.last_name)


	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return (APP_NAME+"_profile", (), { 'username':self.user.username})
	get_absolute_url = models.permalink(get_absolute_url)

class ProfilePic(models.Model):
	"""
		Model for a users profile pic.
	"""
	image = ThumbnailerImageField(upload_to='profilepic/%Y/%b/%d', blank=True)
	user = models.OneToOneField(User, related_name="profile_pic")
	valid = models.BooleanField(default=True)

	class Meta:
		unique_together = (('user', 'valid'),)

	def __unicode__(self):
		return _("%s %s's Profile Pic") % (self.user.first_name , self.user.last_name)


from registration.signals import user_activated

def create_userprofile(sender, user, request, **kwargs):
	profile = UserProfile.objects.create(user=user)
	profile_pic = ProfilePic.objects.create(user=user)

user_activated.connect(create_userprofile)

