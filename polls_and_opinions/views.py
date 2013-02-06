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

APP_NAME = 'polls_and_opinions'

def poll_detail(request, poll_id, template=APP_NAME+"/poll_detail.html"):
    '''
        Displays the poll and its statistics.
        does not allow voting on the poll yet
    '''
    # get the poll object corresponding to the provided poll id
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
                                        },context_instance= RequestContext(request))


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
