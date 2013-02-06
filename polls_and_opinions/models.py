'''
    Models for polls_and_opinions app
'''

__author__ = 'Raj Kamal Singh'
__email__ = 'rkssisodiya@gmail.com'
__status__ = 'development'

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Opinion(models.Model):
    '''
    A doxa opinion. An opinion is intended to be very generic and is expected to be associated 
    with all kinds of models - Polls, images, articles etc, anything.
    '''
    created_on = models.DateTimeField(verbose_name=_("Time of Creation"),auto_now_add=True)
    author = models.ForeignKey(User)
    text = models.TextField()
    
    # Since an opinion can be associated with a variety of stuff, not just polls,
    # contenttypes framework is used here for generic relations
    # These three fields together define a generic foreign key relationship
    # the names for the variables should not be changed, the defaults have been used here.
    # if non-default names are used,they will have to be mentioned in the models
    # that include a reverse generic relation to this model.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type','object_id')
    
    class Meta:
        ordering = ['-created_on']
    
    def __unicode__(self):
        return truncate_text(self.text,50)
        
    def get_absolute_url(self):
        return ('doxa_polls_and_opinions_opinion_detail',(),{
                                    'id' : self.id
                                    })
    get_absolute_url = models.permalink(get_absolute_url)    


# Create your models here.
class Poll(models.Model):
    '''
    Represents a poll in Doxa.
    '''
    question = models.CharField(max_length=500)
    
    # Time of creation is recorded automatically, its not and editable field
    created_on = models.DateTimeField(verbose_name=_("Time of creation"),auto_now_add=True)
    last_modified_on = models.DateTimeField(verbose_name=_("Last modification"), auto_now=True)
    
    # Poll duration etc are all in effect from this date 
    published_on = models.DateTimeField(verbose_name=_("Published on"), blank=True,null=True)
    
    is_live = models.BooleanField(verbose_name=_("live"), default=False)
    duration = models.PositiveIntegerField(verbose_name=_("Poll Duration (days)"), default=0)
    
    author = models.ForeignKey(User)
    # opinions can be associated with polls.
    opinions = generic.GenericRelation(Opinion)
    
    def __unicode__(self):
        return truncate_text(self.question, 50)
    
    def get_absolute_url(self):
        return ('doxa_polls_and_opinions_poll_detail',(),{
                                    'id' : self.id
                                    })
    get_absolute_url = models.permalink(get_absolute_url)    
    
    class Meta:
        ordering = ['-published_on']
        
class Choice(models.Model):
    '''
    A choice for a doxa Poll
    '''
    created_on = models.DateTimeField(verbose_name=_("Time of Creation"),auto_now_add=True)
    last_modified_on = models.DateTimeField(verbose_name=_("Last Modification"),auto_now=True)
    
    # Since users of our app can add new choices,
    author = models.ForeignKey(User)
    
    text = models.CharField(max_length = 100)
    poll = models.ForeignKey(Poll, related_name="choices")
    
    #All choices submitted by users maynot be deemed appropriate by the poll author
    is_approved = models.BooleanField(verbose_name=_("Approved"),default = False)
    
    def __unicode__(self):
        return truncate_text(self.text, 50)

class Vote(models.Model):
    '''
    A vote for a choice
    '''
    created_on = models.DateTimeField(verbose_name=_("Time of Creation"),auto_now_add=True)
    voter = models.ForeignKey(User)
    choice = models.ForeignKey(Choice, related_name=_("votes"))
    
    def __unicode__(self):
        return "%s voted for %s on - %s" % (self.voter,self.choice, self.choice.poll )
    
    def clean(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        # A person should be able to cast only one vote per poll.
        try:
            vote = Vote.objects.get(choice__poll = self.choice.poll,voter=self.voter)
        except Vote.DoesNotExist:
            vote = None
            
        if not vote is None:
            raise ValidationError("A person can cast only one vote per poll. %s has already\
                        voted for \"%s\", for the poll \"%s\""%(self.voter.username,vote.choice,self.choice.poll))
        
        # Call the default validate_unique
        super(Vote,self).clean(*args, **kwargs)

def truncate_text(text, max_length):
    '''
    Utility method to truncate text beyond a certain length
    '''
    if len(text) > max_length -4:
        return text[:max_length-4]+"... "
    else:
        return text