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
	poll = models.ForeignKey(Poll, related_name="choices")
	
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
	choice = models.ForeignKey(Choice, related_name="votes")
	
	def __unicode__(self):
		return "%s voted for %s on - %s" % (voter,choice, choice.poll )
	
	def validate_unique(self, *args, **kwargs):
		from django.core.exceptions import ValidationError
		# A person should be able to cast only one vote per poll.
		try:
			votes = Vote.objects.get(choice__poll = self.choice.poll,voter=self.voter)
		except Vote.DoesNotExist:
			votes = None
			
		if not votes is None:
			raise ValidationError("A person can cast only one vote per poll. The user %s has already\
						voted for %s, for the poll %s"%(self.voter.username,self.choice,self.choice.poll))
		
		# Call the default validate_unique
		super(Vote,self).validate_unique(*args, **kwargs)

class Opinion(models.Model):
	'''
	A doxa opinion. An opinion is intended to be very generic and is expected to be associated 
	with all kinds of models - Polls, images, articles etc, anything.
	'''
	created_on = models.DateTimeField(verbose_name="Time of Creation",auto_now_add=True)
	author = models.ForeignKey(User)
	text = models.TextField()
	