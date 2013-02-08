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


def poll_detail_unauthenticated(request,poll_id, template):
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
                                        #'authenticated' : False,
                                        },context_instance= RequestContext(request))



@login_required
def poll_detail_authenticated(request,poll_id, template):
    '''
        Returns a page for voting.
    '''
    poll = get_object_or_404(Poll,id=poll_id)
    close_date = poll.published_on + timedelta(days=poll.duration)
    # See if a vote exists for this poll for the current user.
    try:
        vote = Vote.objects.get(voter=request.user,choice__poll=poll)
        existing_choice = vote.choice
    except Vote.DoesNotExist:
        vote = None
        existing_choice = None
        
    # If we are processing a submitted form,
    if request.method == "POST":
        # Poll was posted.
        vote_form =PollVoteForm(poll,data=request.POST)
        # Make sure that the poll submitted in the form and the poll id of this
        # url match, if they dont, then just use an empty form
        is_valid = vote_form.is_valid()     # is_valid must be called specially here in order to trigger the cleaning
        if not ( vote_form.cleaned_data.get('poll_id','-1') == poll_id):
            vote_form = get_poll_vote_form(poll,existing_choice)
        elif is_valid:
            # If a correct form was posted, handle the new vote.
            choice = vote_form.cleaned_data['choice']
            # Make sure that the submitted choice and the Poll match
            if not choice.poll == poll:
                vote_form = get_poll_vote_form(poll,existing_choice)
            # If we have reached here then everything is in order. Process the vote.
            # If the current had an existing vote, edit it
            if not vote is None:
                vote.choice = choice
                vote.save()
            # else create a new vote
            else:
                vote = Vote(voter = request.user, choice = choice)
                vote.save()
                
    else:
        vote_form = get_poll_vote_form(poll,existing_choice)
    
    return render_to_response(template,{
                                        'poll':poll,
                                        'close_date':close_date,
                                        'vote_form' : vote_form,
                                        'opinions' : poll.opinions.all(),
                                        #'authenticated' :True,
                                        },context_instance= RequestContext(request))
    


def poll_detail(request, poll_id,template=APP_NAME+"/poll_detail.html"):
    '''
        returns appropriate response depending on whether the user is
        logged in or not.
    '''
    if request.user.is_authenticated():
        return poll_detail_authenticated(request,poll_id, template)
    else:
        return poll_detail_unauthenticated(request, poll_id, template)

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
