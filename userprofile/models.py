from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from easy_thumbnails.fields import ThumbnailerImageField
from userprofile.countries import CountryField
import os

GENDER_CHOICES = ( ('F', _('Female')), ('M', _('Male')),)

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

	def __unicode__(self):
		return _("%s %s's profile") % (self.user.first_name, self.user.last_name)

class ProfilePic(models.Model):
	"""
		Model for a users profile pic.
	"""
	image = ThumbnailerImageField(upload_to='profilepic/%Y/%b/%d', blank=True)
	user = models.OneToOneField(User, related_name="profile_pic")
	valid = models.BooleanField()

	class Meta:
		unique_together = (('user', 'valid'),)

	def __unicode__(self):
		return _("%s %s's Profile Pic") % (self.user.first_name , self.user.last_name)
