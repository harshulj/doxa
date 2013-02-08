'''
    Models for polls_and_opinions app
'''
from django.contrib.auth.decorators import login_required

__author__ = 'Raj Kamal Singh'
__email__ = 'rkssisodiya@gmail.com'
__status__ = 'development'

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from datetime import datetime,timedelta

from models import *
from forms import *

APP_NAME = 'polls_and_opinions'


def poll_detail_unauthenticated(request,poll_id):
    '''
        Returns page for poll and its statistics for an unauthenticated user.
        does not allow voting on the poll, just shows the poll stats
    '''
    poll = get_object_or_404(Poll,id=poll_id)
    
    close_date = poll.published_on + timedelta(days=poll.duration)
    choices = []
    for choice in poll.choices.all():
        choices.append({
                        'text' : choice.text,
                        'votes' : len(choice.votes.all())
                        })    
    
    return render_to_response(template,{
                                        'poll':poll,
                                        'close_date':close_date,
                                        'choices' : choices,
                                        'opinions' : poll.opinions.all(),
                                        },context_instance= RequestContext(request))
@login_required
def poll_detail_authenticated(request,poll_id):
    '''
        Returns a page for voting.
    '''
    poll = get_object_or_404(Poll,id=poll_id)
    close_date = poll.published_on + timedelta(days=poll.duration)
    
    try:
        vote = Vote.objects.get(voter=request.user,choice__poll=poll)
        vote_form = PollVoteForm(poll,initial={'choice':vote.choice})
    except Vote.DoesNotExist:
        vote_form = PollVoteForm(poll)
    
    return render_to_response(template,{
                                        'poll':poll,
                                        'close_date':close_date,
                                        'vote_form' : vote_form,
                                        'opinions' : poll.opinions.all(),
                                        },context_instance= RequestContext(request))
    


def poll_detail(request, poll_id):
    '''
        returns appropriate response depending on whether the user is
        logged in or not.
    '''
    if request.user.is_authenticated():
        return poll_detail_authenticated(request,poll_id)
    else:
        return poll_detail_unauthenticated(request, poll_id)

def poll_list(request, template=APP_NAME+"/polls_list.html"):
    '''
    Displays the list of all polls
    '''
    polls = []
    for poll in Poll.objects.all():
        polls.append({
                      'poll' : poll,
                      'votes' : sum([len(choice.votes.all()) for choice in poll.choices.all()]),
                      })
    return render_to_response(template,{
                                        'polls':polls,
                                        },context_instance= RequestContext(request))
