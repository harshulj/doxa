from django import forms
from models import *

class PollModelChoiceField(forms.ModelChoiceField):
    '''
        Special model choice for the Choice field in the PollVoteForm.
        This is to enable us to create dynamic labels on the fly for the
        choice field.
    '''
    def label_from_instance(self, obj):
        return "%s  (%s)"%(obj.__unicode__(),len(obj.votes.all()))
        

class PollVoteForm(forms.Form):
    '''
        Form for rendering a poll for voting.
        The keyword argument 'poll' must be specified for sure.
        The form is dynamically created based on the poll specified.
    '''
    # This field must be initialized with the appropriate poll id whenever it is created.    
    def __init__(self, poll,*args, **kwargs):  
        super(PollVoteForm,self).__init__(*args,**kwargs)      
        
        # introduce both the poll as a hidden field.
        self.fields['poll_id'] = forms.CharField(widget=forms.HiddenInput)
        self.fields['poll_id'].initial = poll.id
        
        # Choices are presented as a choice field in radio select
        self.fields['choice'] = PollModelChoiceField(label="Choices",queryset=poll.choices.all(), widget=forms.RadioSelect)
        # If an initial value was specified for the choices
        if kwargs.has_key('initial') and kwargs['initial'].has_key('choice'):
            self.fields['choice'].initial = kwargs['initial']['choice']
        # Get rid of the empty choice ( ------ )
        self.fields['choice'].empty_label = None

def get_poll_vote_form(poll,choice=None):
    '''
        Helper method that creates and appropriate PollVoteForm
        If a valid choice is specified, the choice is put in as the initial
        value
    '''
    if ( not choice is None ) and choice.poll == poll:
        return PollVoteForm(poll,initial={'choice' : choice})
    else:
        return PollVoteForm(poll)
    
    
class OpinionForm(forms.Form):
    '''
    Form for creating an opinion.
    '''
    pass