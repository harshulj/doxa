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
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.db import transaction
from django.utils import timezone

from models import *
from forms import *

APP_NAME = 'polls_and_opinions'


#Helper method to do get_object_or_404 for polls with db optimization
def get_poll_or_404(poll_id):
    '''
    Does a select related query for Poll and returns 404 if not found.
    '''
    try:
        poll = Poll.objects.prefetch_related('opinions').get(id=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return poll

def poll_detail_unauthenticated(request,poll_id, template):
    '''
        Returns page for poll and its statistics for an unauthenticated user.
        does not allow voting on the poll, just shows the poll stats
    '''
    poll = get_poll_or_404(poll_id)
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
def vote_submit(request,id):
    '''
        Handles submission of a poll vote form
    '''
    if not request.method == 'POST':
        return HttpResponseRedirect(reverse(APP_NAME+"_poll_detail", kwargs={'id':id}))
    poll = get_poll_or_404(id)
    # See if a vote exists for this poll for the current user.
    try:
        vote = Vote.objects.select_related().get(voter=request.user,choice__poll=poll)
        existing_choice = vote.choice
    except Vote.DoesNotExist:
        vote = None
        existing_choice = None
    # Default form objects. If things have been posted, these variables will get appropriate values
    vote_form =PollVoteForm(poll,data=request.POST)
    # Make sure that the poll submitted in the form and the poll id of this
    # url match, if they dont, then just use an empty form
    is_valid = vote_form.is_valid()     # is_valid must be called specially here in order to trigger the cleaning
    
    if not ( vote_form.cleaned_data.get('poll_id','-1') == id):
        return HttpResponseRedirect(reverse(APP_NAME+"_poll_detail", kwargs={'id':id}))
    elif is_valid:
        choice = vote_form.cleaned_data['choice']
        # Make sure that the submitted choice and the Poll match, disabling this check will reduce a db hit
        if not choice.poll == poll:
            vote_form = get_poll_vote_form(poll,existing_choice)
        
        if not vote is None:    #if a vote already exists for this poll
            vote.choice = choice
            vote.save()
        # else create a new vote
        else:
            vote = Vote(voter = request.user, choice = choice)
            vote.save()
    return HttpResponseRedirect(reverse(APP_NAME+"_poll_detail", kwargs={'id':id}))

@login_required
def poll_opinion_submit(request,id):
    '''
        Handles submission of an opinion on a poll
    '''
    if not request.method == 'POST':
        return HttpResponseRedirect(reverse(APP_NAME+"_poll_detail", kwargs={'id':id}))
    poll = get_poll_or_404(id)
    # Get the contenttype for Poll, to be used for the Opinion
    poll_type = ContentType.objects.get(app_label=APP_NAME,model="Poll")
    opinion_form = OpinionForm(request.POST)
    is_valid = opinion_form.is_valid() #trigger the cleaning

    # Make sure that the submitted opinion form was for this poll only and other validation
    if (not opinion_form.cleaned_data.get('content_type_id','-1') == poll_type.id) \
        or ( not opinion_form.cleaned_data.get('object_id','-1') == poll.id)\
        or (not opinion_form.cleaned_data.get('text','')):
        return HttpResponseRedirect(reverse(APP_NAME+"_poll_detail", kwargs={'id':id}))
    elif is_valid:
        # If the form is valid, then save the opinion to the database.
        text = opinion_form.cleaned_data['text']
        op = Opinion(author=request.user,text=text,content_type=poll_type,object_id=poll.id)
        op.save()
    return HttpResponseRedirect(reverse(APP_NAME+"_poll_detail", kwargs={'id':id}))
    
@login_required
def poll_detail_authenticated(request,poll_id, template):
    '''
        Returns a page for voting.
    '''
    poll = get_poll_or_404(poll_id)
    close_date = poll.published_on + timedelta(days=poll.duration)

    try:
        vote = Vote.objects.select_related().get(voter=request.user,choice__poll=poll)
        existing_choice = vote.choice
    except Vote.DoesNotExist:
        existing_choice = None

    vote_form = get_poll_vote_form(poll,existing_choice)
    
    poll_type = ContentType.objects.get(app_label=APP_NAME,model="Poll")
    opinion_form = OpinionForm(initial={'content_type_id':poll_type.id,'object_id':poll.id})
    
    return render_to_response(template,{
                                        'poll':poll,
                                        'close_date':close_date,
                                        'vote_form' : vote_form,
                                        'opinions' : poll.opinions.all(),
                                        'opinion_form' : opinion_form,
                                        #'authenticated' :True,
                                        },context_instance= RequestContext(request))
    


def poll_detail(request, id,template=APP_NAME+"/poll_detail.html"):
    '''
        returns appropriate response depending on whether the user is
        logged in or not.
    '''
    if request.user.is_authenticated():
        return poll_detail_authenticated(request,id, template)
    else:
        return poll_detail_unauthenticated(request, id, template)

def poll_list(request, template=APP_NAME+"/polls_list.html"):
    '''
    Displays the list of all polls
    '''
    polls = []
    for poll in Poll.objects.prefetch_related('choices__votes').all():
        polls.append({
                      'poll' : poll,
                      'votes' : sum([len(choice.votes.all()) for choice in poll.choices.all()]),
                      })
    return render_to_response(template,{
                                        'polls':polls,
                                        },context_instance= RequestContext(request))


@login_required
@transaction.commit_on_success
def create_poll(request):
    '''
    View for allowing a user to create a poll and to also add choices to it.
    '''
    ChoiceFormset = formset_factory(ChoiceForm, extra=1)
    if request.method == "POST":
        poll_form = PollForm(request.POST)
        choice_forms = ChoiceFormset(request.POST)
        if poll_form.is_valid() and choice_forms.is_valid():
            # Create Poll and associated choices
            poll = poll_form.save(commit=False)
            poll.author = request.user
            if poll.published_on is None:
                poll.published_on = timezone.now()
            poll.save()
            for choice_form in choice_forms.cleaned_data:
                choice = Choice.objects.create(author=request.user,text=choice_form['text'],\
                                               poll=poll)
            return HttpResponseRedirect(reverse(APP_NAME+"_poll_detail", kwargs={'id':poll.id}))
    else:
        poll_form = PollForm()
        choice_forms = ChoiceFormset()
        
    return render_to_response(APP_NAME+"/create_poll.html",{
                                        'poll_form' : poll_form,
                                        'choice_forms' : choice_forms,
                                        },context_instance= RequestContext(request))
    