'''
    Models for polls_and_opinions app
'''
from django.core.context_processors import request

__author__ = 'Raj Kamal Singh'
__email__ = 'rkssisodiya@gmail.com'
__status__ = 'development'
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
import tagging
from tagging.models import TaggedItem
from djangoratings.fields import RatingField
from recommends.providers import recommendation_registry, RecommendationProvider
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from signals import *

APP_NAME = 'polls_and_opinions'

class Opinion(models.Model):
    '''
    A doxa opinion. An opinion is intended to be very generic and is expected to be associated 
    with all kinds of models - Polls, images, articles etc, anything.
    '''
    created_on = models.DateTimeField(verbose_name=_("Time of Creation"),auto_now_add=True)
    author = models.ForeignKey(User)
    text = models.TextField()
    
    #Tags for this opinion based on the generic django-tagging application
    tags = tagging.fields.TagField()
    
    # Since an opinion can be associated with a variety of stuff, not just polls,
    # contenttypes framework is used here for generic relations
    # These three fields together define a generic foreign key relationship
    # the names for the variables should not be changed, the defaults have been used here.
    # if non-default names are used,they will have to be mentioned in the models
    # that include a reverse generic relation to this model.
    # An opinion may and may not be associated with an object, hence the contenttype and object id can be null
    content_type = models.ForeignKey(ContentType, blank=True, null = True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = generic.GenericForeignKey('content_type','object_id')
    
    # Rating field for rating of opinions. For now, opinions will be either have an upvote or
    # a downvote. so the separate property for upvote, downvote will be based on that.
    # if rating is not set, then vote is 0, if rating is 1, vote is -1 (downvote) else
    # if rating is 2, vote is +1 (upvote)
    __rating = RatingField(range=2, can_change_vote=True, allow_delete=True)

    # The Vote property of the Opinion is the one to be used    
    def get_vote_for_user(self,user):
        rating = self.__rating.get_rating_for_user(user)
        if rating is None or rating==0:
            return 0
        elif rating == 1:
            return -1
        else:
            return 1

    def set_vote_for_user(self,request,vote):
        if vote < -1 or vote > 1:
            raise ValueError("An opinion vote must be either 0(no vote),-1(downvote) or 1(upvote)")
        rating = self.__rating.get_rating_for_user(request.user)
        if (not rating is None):
            self.__rating.delete(request.user,request.META['REMOTE_ADDR'])
        if not vote ==0:
            if vote == -1:
                val = 1
            else:
                val = 2
            self.__rating.add(score=val, user=request.user, ip_address=request.META['REMOTE_ADDR'])
    
    def clean(self):
        '''
            custom clean method to make sure that the content_type and object_id 
            both either have values or both are None
        '''
        from django.core.exceptions import ValidationError
        if bool(self.content_type) ^ bool(self.object_id):
            raise ValidationError("content_type and object_id must either both be set or both unset,\
                    content_type has value %s and \n\
                    object_id has value %s"%(self.content_type,self.object_id))
        
    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True
        super(Opinion,self).save(*args,**kwargs)
        #If the model got successfully saved and this is a newly created
        #instance, emit a signal
        if new:
            opinion_created.send(sender = self)
    
    class Meta:
        ordering = ['-created_on']
    
    def __unicode__(self):
        return truncate_text(self.text,50)
        
    def get_absolute_url(self):
        return (APP_NAME+'_opinion_detail',(),{
                                    'id' : self.id
                                    })
    get_absolute_url = models.permalink(get_absolute_url)    


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
    
    # tags for this poll
    tags = tagging.fields.TagField()
    
    # Ratings of polls can go from 1 to 5
    rating = RatingField(range=5, can_change_vote=True, allow_delete=True)
    
    def __unicode__(self):
        return truncate_text(self.question, 50)
    
    def get_absolute_url(self):
        return (APP_NAME+'_poll_detail',(),{
                                    'id' : self.id
                                    })
    get_absolute_url = models.permalink(get_absolute_url)    
    
    class Meta:
        ordering = ['-published_on']
        
    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True
        super(Poll,self).save(*args,**kwargs)
        #If the model got successfully saved and this is a newly created
        #instance, emit a signal
        if new:
            poll_created.send(sender = self)
        
        
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
    
    # Ratings of polls can go from 1 to 5
    rating = RatingField(range=5, can_change_vote=True, allow_delete=True)    
    
    def __unicode__(self):
        return truncate_text(self.text, 50)
    
    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True
        super(Choice,self).save(*args,**kwargs)
        #If the model got successfully saved and this is a newly created
        #instance, emit a signal
        if new:
            choice_created.send(sender = self)
 

class Vote(models.Model):
    '''
    A vote for a choice
    '''
    created_on = models.DateTimeField(verbose_name=_("Time of Creation"),auto_now_add=True)
    voter = models.ForeignKey(User)
    choice = models.ForeignKey(Choice, related_name="votes")
    
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

    def save(self, *args, **kwargs):
        voted.send(sender = self)



def truncate_text(text, max_length):
    '''
    Utility method to truncate text beyond a certain length
    '''
    if len(text) > max_length -4:
        return text[:max_length-4]+"... "
    else:
        return text
    
# Helper methods to retrieve polls and opinions by tags.
def get_opinions_for_tags(tags):
    '''
    Returns all the opinions for the supplied tags
    The tags are expected to be in a string - either space separated or comma separated
    '''
    return TaggedItem.objects.get(Opinion,tags)

def get_polls_for_tags(tags):
    '''
    Returns all the polls for the supplied tags
    The tags are expected to be in a string - either space separated or comma separated
    '''    
    return TaggedItem.objects.get(Poll,tags)

# Recommendation provider for polls.
class PollRecommendationProvider(RecommendationProvider):
    def get_users(self):
        return User.objects.filter(is_active=True, votes__isnull=False).distinct()

    def get_items(self):
        return Poll.objects.all()

    def get_ratings(self, obj):
        return obj.rating.get_ratings()

    def get_rating_score(self, rating):
        return rating.score

    def get_rating_user(self, rating):
        return rating.user

    def get_rating_item(self, rating):
        return rating.content_object

recommendation_registry.register(Vote, [Poll], PollRecommendationProvider)
