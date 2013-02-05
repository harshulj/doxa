from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Poll(models.Model):
	'''
	Represents a poll in Doxa.
	'''
	question = models.CharField(max_length=500)
	
	# The slug ideally gets prepopulated from the question - it basically helps in creating 
	# descriptive urls for polls. The directive for prepopulation of the slug must be given in the 
	# modeladmin for this model.
	slug = models.SlugField(unique=True, help_text="Gets automatically prepopulated from the question",
						max_length=80)
	# Time of creation is recorded automatically, its not and editable field
	created_on = models.DateTimeField(verbose_name="Time of creation",auto_now_add=True)
	last_modified_on = models.DateTimeField(verbose_name="Last modification", auto_now=True)
	
	# Poll duration etc are all in effect from this date 
	published_on = models.DateTimeField(verbose_name="Published on", blank=True,null=True)
	
	is_live = models.BooleanField(verbose_name="live", default=False)
	duration = models.PositiveIntegerField(verbose_name="Poll Duration", default=0)
	
	author = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.slug
	
	def get_absolute_url(self):
		return ('doxa_polls_poll_detail',(),{
									'created_on' : self.created_on,
									'published_on' : self.published_on,
									'slug' : self.slug
									})
	get_absolute_url = models.permalink(get_absolute_url)	
	
	class Meta:
		ordering = ['-published_on']
		
class Choice(models.Model):
	'''
	A choice for a doxa Poll
	'''
	created_on = models.DateTimeField(verbose_name="Time of Creation",auto_now_add=True)
	last_modified_on = models.DateTimeField(verbose_name="Last Modification",auto_now=True)
	
	# Since users of our app can add new choices,
	author = models.ForeignKey(User)
	
	text = models.CharField(max_length = 100)
	poll = models.ForeignKey(Poll)
	
	#All choices submitted by users maynot be deemed appropriate by the poll author
	is_approved = models.BooleanField(verbose_name="Approved",default = False)
	
	def __unicode__(self):
		if len(text) > 45:
			return self.text[:45] + "... "
		else:
			return self.text

class Vote(models.Model):
	'''
	A vote for a choice
	'''
	created_on = models.DateTimeField(verbose_name="Time of Creation",auto_now_add=True)
	voter = models.ForeignKey(User)
	choice = models.ForeignKey(Choice)

#TODO: A user should be allowed to cast only one vote for a poll
# If no soln is found, override save and raise an error if integrity violated

class Opinion(models.Model):
	'''
	A doxa opinion. An opinion is intended to be very generic and is expected to be associated 
	with all kinds of models - Polls, images, articles etc, anything.
	'''
	created_on = models.DateTimeField(verbose_name="Time of Creation",auto_now_add=True)
	author = models.ForeignKey(User)
	text = models.TextField()